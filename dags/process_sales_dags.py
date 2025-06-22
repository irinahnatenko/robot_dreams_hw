from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

with DAG(
    "process_sales_dag",
    schedule_interval=None,
    start_date=datetime(2023, 1, 1),
    catchup=False
) as dag:

    run_spark_job = DockerOperator(
        task_id="run_process_sales",
        image="spark-image:latest",
        api_version='auto',
        auto_remove=True,
        command="spark-submit /home/jovyan/spark_jobs/process_sales.py",
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge"
    )