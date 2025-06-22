from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

with DAG(
    "enrich_user_profiles_dag",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False
) as dag:

    run_enrich = BashOperator(
        task_id="run_enrich_user_profiles",
        bash_command="docker exec final_work-spark-1 spark-submit /home/jovyan/spark_jobs/enrich_user_profiles.py"
    )
