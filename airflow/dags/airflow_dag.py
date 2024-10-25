from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id = "DE_project",
    default_args = {
        "retries": 3,
        "retry_delay": timedelta(minutes=5)
    },
    description = "ETL process",
    start_date = datetime(2024, 10, 25),
    schedule_interval = '0 7 * * *'
) as dag:
    
    t1 = BashOperator(
        task_id = "Data_generation",
        bash_command = "cd ~ && cd airflow && cd py && echo 'Start generating data' && python3 faking_data.py && echo 'Data generation completed'",
    )

    t2 = BashOperator(
        task_id = "ETL",
        bash_command = "cd ~ && cd airflow && cd py && echo 'Start ETL data' && python3 etl_process.py && echo 'ETL completed'",
    )

    t1 >> t2