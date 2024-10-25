# Real-time processing of user interaction logs on the website from a recruitment platform.

## Objective

The project aims to build a near-real-time data processing system focused on analyzing and optimizing the performance of online advertising campaigns. By collecting, transforming, and storing data from various sources, the system will provide insights into key metrics such as clicks, impressions, and advertising costs. As a result, campaign managers can make more informed decisions, improve advertising performance, and enhance budget spending efficiency.

## Tools & Technologies

- [**Kafka**](https://kafka.apache.org)
- [**PySpark**](https://spark.apache.org/docs/latest/api/python/index.html)
- [**Airflow**](https://airflow.apache.org)
- [**Grafana**](https://grafana.com/)
- [**Linux Command**]()
- [**MySQL**](https://www.mysql.com/)
- [**Cassandra**](https://cassandra.apache.org/_/index.html)
- [**Python**](https://www.python.org/)

## Architecture

![image atl](https://github.com/tuankhoi25/Near-real-time-data-pipeline/blob/d6054aca249ffaa63b59fbd74f62c0770efec696/architecture.png)

## Raw Data

```sh
root
 |-- create_time: string (nullable = false)
 |-- bid: integer (nullable = true)
 |-- bn: string (nullable = true)
 |-- campaign_id: integer (nullable = true)
 |-- cd: integer (nullable = true)
 |-- custom_track: string (nullable = true)
 |-- de: string (nullable = true)
 |-- dl: string (nullable = true)
 |-- dt: string (nullable = true)
 |-- ed: string (nullable = true)
 |-- ev: integer (nullable = true)
 |-- group_id: integer (nullable = true)
 |-- id: string (nullable = true)
 |-- job_id: integer (nullable = true)
 |-- md: string (nullable = true)
 |-- publisher_id: integer (nullable = true)
 |-- rl: string (nullable = true)
 |-- sr: string (nullable = true)
 |-- ts: string (nullable = true)
 |-- tz: integer (nullable = true)
 |-- ua: string (nullable = true)
 |-- uid: string (nullable = true)
 |-- utm_campaign: string (nullable = true)
 |-- utm_content: string (nullable = true)
 |-- utm_medium: string (nullable = true)
 |-- utm_source: string (nullable = true)
 |-- utm_term: string (nullable = true)
 |-- v: integer (nullable = true)
 |-- vp: string (nullable = true)
 ```

## Processed Data

```sh
root
 |-- job_id: integer (nullable = true)
 |-- dates: timestamp (nullable = true)
 |-- hours: integer (nullable = true)
 |-- publisher_id: integer (nullable = true)
 |-- company_id: integer (nullable = true)
 |-- campaign_id: integer (nullable = true)
 |-- group_id: integer (nullable = true)
 |-- disqualified_application: integer (nullable = true)
 |-- qualified_application: integer (nullable = true)
 |-- conversion: integer (nullable = true)
 |-- clicks: integer (nullable = true)
 |-- bid_set: double (nullable = true)
 |-- spend_hour: double (nullable = true)
 |-- sources: string (nullable = true)
 |-- latest_update_time: timestamp (nullable = true)
 ```

## Final Result

![image atl](https://github.com/tuankhoi25/Near-real-time-data-pipeline/blob/0a889563ee1131d49af0dd19da8f7743c8d29e16/architecture.png)
