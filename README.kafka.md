# Get the software on local machine

- Download Confluent Platform using only Confluent Community components directly by using the curl command in a terminal.
    ```sh
    curl -O https://packages.confluent.io/archive/7.7/confluent-community-7.7.1.zip
    ```
- Extract the contents of the archive. For ZIP files, run this command.
    ```sh
    unzip confluent-7.7.1.zip
    ```
- Configure CONFLUENT_HOME and PATH
  ```sh
  export CONFLUENT_HOME=~/confluent-7.7.1
  export PATH=$PATH:$CONFLUENT_HOME/bin
  ```

# Start the Kafka environment with ZooKeeper
- Open new terminal. Run the following command in order to start all services in the correct order:
  ```sh
  $CONFLUENT_HOME/bin/zookeeper-server-start $CONFLUENT_HOME/etc/kafka/zookeeper.properties
  ```
- Open new terminal session and run:
  ```sh
  $CONFLUENT_HOME/bin/kafka-server-start $CONFLUENT_HOME/etc/kafka/server.properties
  ```
- Open new terminal. Create a topic to store your events:
  ```sh
  $CONFLUENT_HOME/bin/kafka-topics --create --topic events --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
  ```

#  Start the Kafka Schema Registry service
- Open new terminal and run this command:
  ```sh
  $CONFLUENT_HOME/bin/schema-registry-start $CONFLUENT_HOME/etc/schema-registry/schema-registry.properties
  ```

# Start ksqlDB
- Open new terminal. Start ksqlDB's server:
  ```sh
  $CONFLUENT_HOME/bin/ksql-server-start $CONFLUENT_HOME/etc/ksqldb/ksql-server.properties
  ```
- Open new terminal. Start ksqlDB's interactive CLI:
  ```sh
  $CONFLUENT_HOME/bin/ksql http://localhost:8088
  ```
- Open ksqlDB's interactive CLI terminal. Create streams:
  ```sql
  CREATE STREAM events_as_json (
     job_id DOUBLE,
     dates STRING,
     "hours" INTEGER,
     publisher_id DOUBLE,
     company_id INTEGER,
     campaign_id DOUBLE,
     group_id DOUBLE,
     disqualified_application BIGINT,
     qualified_application BIGINT,
     conversion BIGINT,
     clicks BIGINT,
     bid_set DOUBLE,
     spend_hour DOUBLE,
     sources STRING
  ) WITH (
     KAFKA_TOPIC = 'events',
     VALUE_FORMAT = 'JSON'
  );
  
  SET 'auto.offset.reset' = 'earliest';
  
  CREATE STREAM events_as_avro
    WITH (VALUE_FORMAT='AVRO') AS
      SELECT * FROM events_as_json;
  ```
# Set-up for Kafka Connect
## Install Kafka Connect connector plugins
- Installing connector manually from this link: https://www.confluent.io/hub/confluentinc/kafka-connect-jdbc
- Extract the ZIP file contents:
  ```sh
  unzip confluentinc-kafka-connect-jdbc-10.8.0.zip
  ```
- Move the contents to the desired location:
  ```sh
  mkdir -p $CONFLUENT_HOME/connectors
  mv confluentinc-kafka-connect-jdbc-10.8.0 $CONFLUENT_HOME/connectors/
  ```
- Add this to the plugin path in your Connect properties file:
  ```sh
  echo -e "\nplugin.path=/usr/share/java,$CONFLUENT_HOME/connectors" >> $CONFLUENT_HOME/etc/kafka/connect-standalone.properties
  ```
  
## Installing a JDBC driver for the Kafka Connect JDBC connector
- Open new terminal. Installing JDBC driver on local:
  ```sh
  curl -O https://repo1.maven.org/maven2/com/mysql/mysql-connector-j/8.3.0/mysql-connector-j-8.3.0.jar
  ```
- Move to the desired location:
  ```sh
  mv mysql-connector-j-8.3.0.jar $CONFLUENT_HOME/connectors/confluentinc-kafka-connect-jdbc-10.8.0/lib
  ```

## Start Kafka Connect in standalone mode
- Open new terminal. Run this command:
  ```sh
  connect-standalone $CONFLUENT_HOME/etc/kafka/connect-standalone.properties
  ```

## Create a JDBC Sink Connector in Kafka Connect
- Open new terminal. Run this command:
  ```sh
  curl -X PUT http://localhost:8083/connectors/sink-jdbc-mysql-01/config \
         -H "Content-Type: application/json" -d '{
        "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
        "connection.url": "jdbc:mysql://localhost:3306/DE_project",
        "topics": "EVENTS_AS_AVRO",
        "key.converter": "org.apache.kafka.connect.storage.StringConverter",
        "value.converter": "io.confluent.connect.avro.AvroConverter",
        "value.converter.schema.registry.url": "http://localhost:8081",
        "connection.user": "root",
        "connection.password": "1",
        "auto.evolve": true,
        "auto.create": true,
        "insert.mode": "insert",
        "table.name.format": "events"
    }'
    ```
