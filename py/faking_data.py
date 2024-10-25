import time
import random
import datetime
import pandas as pd
from sqlalchemy import create_engine
import cassandra
from cassandra.cluster import Cluster

def get_data_from_job(engine):
    query = """select id as job_id, campaign_id, group_id, company_id from job"""
    mysql_data = pd.read_sql(query, engine)
    return mysql_data

def get_data_from_publisher(engine):
    query = """select distinct(id) as publisher_id from master_publisher"""
    mysql_data = pd.read_sql(query, engine)
    return mysql_data

def generating_dummy_data(n_records, session, engine):
    publisher = get_data_from_publisher(engine)
    publisher = publisher['publisher_id'].to_list()
    jobs_data = get_data_from_job(engine)
    job_list = jobs_data['job_id'].to_list()
    campaign_list = jobs_data['campaign_id'].to_list()
    group_list = jobs_data[jobs_data['group_id'].notnull()]['group_id'].astype(int).to_list()

    for _ in range(0, n_records + 1):
        create_time = str(cassandra.util.uuid_from_time(datetime.datetime.now()))
        bid = random.randint(0,1)
        interact = ['click','conversion','qualified','unqualified']
        custom_track = random.choices(interact, weights=(70, 10, 10, 10))[0]
        job_id = random.choice(job_list)
        publisher_id = random.choice(publisher)
        group_id = random.choice(group_list)
        campaign_id = random.choice(campaign_list)
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql = """INSERT INTO tracking (create_time, bid, campaign_id, custom_track, group_id, job_id, publisher_id, ts) VALUES ('{}',{},{},'{}',{},{},{},'{}')""".format(create_time, bid, campaign_id, custom_track, group_id, job_id, publisher_id, ts)
        print(sql)
        session.execute(sql)
    return print("Data Generated Successfully")

def main():
    host = 'localhost'
    db_name = 'DE_project'
    user = 'root'
    password = '1'
    engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{db_name}")

    keyspace = 'DE_project'
    cluster = Cluster()
    session = cluster.connect(keyspace)

    while True:
        generating_dummy_data(n_records=random.randint(1, 10), session=session, engine=engine)
        time.sleep(10)

main()