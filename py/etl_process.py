import time
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import lit

# ----------------------------------------------------------EXTRACT--------------------------------------------------------------

def extract(mysql_time):
    data = spark.read.format("org.apache.spark.sql.cassandra").options(table="tracking", keyspace="DE_project").load().where(col('ts')>= mysql_time)
    data = data.select('ts','job_id','custom_track','bid','campaign_id','group_id','publisher_id')
    data = data.filter(data.job_id.isNotNull())
    return data

# ---------------------------------------------------------TRANSFORM-------------------------------------------------------------

def calculating_clicks(data):
    clicks_data = data.filter(data.custom_track == 'click')
    clicks_data = clicks_data.na.fill({'bid':0})
    clicks_data = clicks_data.na.fill({'job_id':0})
    clicks_data = clicks_data.na.fill({'publisher_id':0})
    clicks_data = clicks_data.na.fill({'group_id':0})
    clicks_data = clicks_data.na.fill({'campaign_id':0})
    clicks_data.createOrReplaceTempView('clicks')
    clicks_output = spark.sql("""select job_id , date(ts) as date , hour(ts) as hour , publisher_id , campaign_id , group_id , avg(bid) as bid_set, count(*) as clicks , sum(bid) as spend_hour from clicks
    group by job_id , date(ts) , hour(ts) , publisher_id , campaign_id , group_id """)
    return clicks_output 

def calculating_conversion(data):
    conversion_data = data.filter(data.custom_track == 'conversion')
    conversion_data = conversion_data.na.fill({'job_id':0})
    conversion_data = conversion_data.na.fill({'publisher_id':0})
    conversion_data = conversion_data.na.fill({'group_id':0})
    conversion_data = conversion_data.na.fill({'campaign_id':0})
    conversion_data.createOrReplaceTempView('conversion')
    conversion_output = spark.sql("""select job_id , date(ts) as date , hour(ts) as hour , publisher_id , campaign_id , group_id , count(*) as conversions from conversion
    group by job_id , date(ts) , hour(ts) , publisher_id , campaign_id , group_id """)
    return conversion_output 

def calculating_qualified(data):    
    qualified_data = data.filter(data.custom_track == 'qualified')
    qualified_data = qualified_data.na.fill({'job_id':0})
    qualified_data = qualified_data.na.fill({'publisher_id':0})
    qualified_data = qualified_data.na.fill({'group_id':0})
    qualified_data = qualified_data.na.fill({'campaign_id':0})
    qualified_data.createOrReplaceTempView('qualified')
    qualified_output = spark.sql("""select job_id , date(ts) as date , hour(ts) as hour , publisher_id , campaign_id , group_id , count(*) as qualified from qualified
    group by job_id , date(ts) , hour(ts) , publisher_id , campaign_id , group_id """)
    return qualified_output

def calculating_unqualified(data):
    unqualified_data = data.filter(data.custom_track == 'unqualified')
    unqualified_data = unqualified_data.na.fill({'job_id':0})
    unqualified_data = unqualified_data.na.fill({'publisher_id':0})
    unqualified_data = unqualified_data.na.fill({'group_id':0})
    unqualified_data = unqualified_data.na.fill({'campaign_id':0})
    unqualified_data.createOrReplaceTempView('unqualified')
    unqualified_output = spark.sql("""select job_id , date(ts) as date , hour(ts) as hour , publisher_id , campaign_id , group_id , count(*) as unqualified  from unqualified
    group by job_id , date(ts) , hour(ts) , publisher_id , campaign_id , group_id """)
    return unqualified_output

def process_final_data(clicks_output, conversion_output, qualified_output, unqualified_output):
    final_data = clicks_output.join(conversion_output,['job_id','date','hour','publisher_id','campaign_id','group_id'],'full') \
        .join(qualified_output,['job_id','date','hour','publisher_id','campaign_id','group_id'],'full') \
        .join(unqualified_output,['job_id','date','hour','publisher_id','campaign_id','group_id'],'full')
    return final_data 

def process_cassandra_data(data):
    clicks_output = calculating_clicks(data)
    conversion_output = calculating_conversion(data)
    qualified_output = calculating_qualified(data)
    unqualified_output = calculating_unqualified(data)
    final_data = process_final_data(clicks_output,conversion_output,qualified_output,unqualified_output)
    return final_data

def retrieve_company_data():
    company = spark.read.format('jdbc') \
        .option("driver","com.mysql.cj.jdbc.Driver") \
        .option("url", "jdbc:mysql://localhost:3306/DE_project") \
        .option("dbtable", """(SELECT id as job_id, company_id, group_id, campaign_id FROM job) test""") \
        .option("user", "root") \
        .option("password", "1") \
        .load()
    return company 

def transform(data):
    cassandra_output = process_cassandra_data(data)
    company = retrieve_company_data()
    final_output = cassandra_output.join(company,'job_id','left').drop(company.group_id).drop(company.campaign_id)
    return final_output

# -----------------------------------------------------Import To Kafka-----------------------------------------------------------

def import_to_kafka(data):
    data = data.select('job_id','date','hour','publisher_id','company_id','campaign_id','group_id','unqualified','qualified','conversions','clicks','bid_set','spend_hour')
    data = data.withColumnRenamed('date','dates') \
        .withColumnRenamed('hour','hours') \
        .withColumnRenamed('qualified','qualified_application') \
        .withColumnRenamed('unqualified','disqualified_application') \
        .withColumnRenamed('conversions','conversion')
    data = data.withColumn('sources',lit('Cassandra'))
    data = data.na.fill({'disqualified_application':0})
    data = data.na.fill({'qualified_application':0})
    data = data.na.fill({'conversion':0})
    data = data.na.fill({'clicks':0})
    data = data.na.fill({'bid_set':0.0})
    data = data.na.fill({'spend_hour':0.0})
    data.selectExpr("CAST(job_id AS STRING) AS key", "to_json(struct(*)) AS value") \
        .write.format("kafka").option("kafka.bootstrap.servers", "localhost:9092").option("topic", "events").save()

# --------------------------------------------------------------ETL--------------------------------------------------------------

def etl_process(mysql_time):
    df = extract(mysql_time)
    print("EXTRACT completed")

    df = transform(df)
    print("TRANSFORM completed")
    
    import_to_kafka(df)
    print("IMPORT TO KAFKA completed")

# -------------------------------------------------------Timestamp-Based CDC-----------------------------------------------------

def get_latest_time_cassandra():
    data = spark.read.format("org.apache.spark.sql.cassandra").options(table='tracking', keyspace='DE_project').load()
    cassandra_latest_time = data.agg({'ts':'max'}).take(1)[0][0]
    return cassandra_latest_time

def get_mysql_latest_time():
    mysql_time = spark.read.format('jdbc') \
        .option("driver","com.mysql.cj.jdbc.Driver") \
        .option("url", "jdbc:mysql://localhost:3306/DE_project") \
        .option("dbtable", """(select max(latest_update_time) from events) data""") \
        .option("user", "root") \
        .option("password", "1") \
        .load()
    mysql_time = mysql_time.take(1)[0][0]

    if mysql_time is None:
        mysql_latest = '1998-01-01 23:59:59'
    else:
        mysql_latest = mysql_time.strftime('%Y-%m-%d %H:%M:%S')
    return mysql_latest 

def cdc():
    while True:
        cassandra_time = get_latest_time_cassandra()
        mysql_time = get_mysql_latest_time()

        if cassandra_time > mysql_time: 
            etl_process(mysql_time)
        else:
            print("No new data found")
        time.sleep(5)

# -------------------------------------------------------------------------------------------------------------------------------

scala_version = '2.12' 
spark_version = '3.4.1'
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.3.1',
    'com.mysql:mysql-connector-j:8.3.0',
    'com.datastax.spark:spark-cassandra-connector_2.12:3.1.0'
    ]

spark = SparkSession.builder \
   .master("local") \
   .appName("kafka-example") \
   .config("spark.jars.packages", ",".join(packages)) \
   .getOrCreate()

cdc()