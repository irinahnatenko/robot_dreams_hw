from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    "process_sales_dag",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False
) as dag:

    run_sales = BashOperator(
        task_id="run_process_sales",
        bash_command="docker exec final_work-spark-1 spark-submit /home/jovyan/spark_jobs/process_sales.py"
    )
