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

<img width="1167" alt="Ảnh màn hình 2024-10-26 lúc 15 11 08" src="https://github.com/user-attachments/assets/a55ccb96-98e7-4e41-869f-47fc34f89226">

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
 |-- job_id: double (nullable = true)
 |-- dates: varchar(20) (nullable = true)
 |-- hours: int (nullable = true)
 |-- publisher_id: double (nullable = true)
 |-- company_id: int (nullable = true)
 |-- campaign_id: double (nullable = true)
 |-- group_id: double (nullable = true)
 |-- disqualified_application: bigint (nullable = true)
 |-- qualified_application: bigint (nullable = true)
 |-- conversion: bigint (nullable = true)
 |-- clicks: bigint (nullable = true)
 |-- bid_set: double (nullable = true)
 |-- spend_hour: double (nullable = true)
 |-- sources: varchar(20) (nullable = true)
 |-- latest_update_time: timestamp (nullable = true)
 ```

## Final Result

<img width="1432" alt="Result" src="https://github.com/user-attachments/assets/04de8e20-c415-4b34-b62d-2b75bd9f82d4">
