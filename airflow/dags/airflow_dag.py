from datetime import datetime, timedelta
from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id = "DE_project",
    default_args = {
        "retries": 19,
        "retry_delay": timedelta(minutes=1)
    },
    description = "ETL process",
    start_date = datetime(2024, 10, 25),
    schedule_interval = '0 7 * * *'
) as dag:

    t1 = BashOperator(
        task_id = "ETL",
        bash_command = "cd ~ && cd airflow && cd py && echo 'Start ETL data' && python3 etl_process.py",
        execution_timeout=timedelta(minutes=30)
    )

    t1
