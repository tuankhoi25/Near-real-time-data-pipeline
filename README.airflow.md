# Airflow Setup

- Open new terminal. Run this command to install Airflow:
  ```sh
  pip install apache-airflow
  ```
- Change directory to the airflow folder:
  ```sh
  cd airflow
  ```
- Set Airflow Home:
  ```sh
  export AIRFLOW_HOME=$(pwd)
  ```
- Create an admin user for the Airflow web interface:
  ```sh
  airflow users create --role Admin --username admin --email admin --firstname admin --lastname admin --password admin
  ```
- Initialize the Airflow metadata database:
  ```sh
  airflow db init
  ```
- Start the Airflow web server:
  ```sh
  airflow webserver -p 8080
  ```
- Open new terminal. Start the Apache Airflow scheduler:
  ```sh
  cd airflow
  airflow scheduler
  ```
