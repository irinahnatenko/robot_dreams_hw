from airflow import DAG
from airflow.utils.dates import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from airflow.exceptions import AirflowFailException

import os
import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 4, 22, 1, 0, 0),
    'end_date': datetime(2025, 4, 24, 1, 0, 0),
    'email_on_failure': True,
    'email': ['hnatenkoirina5@gmail.com'],
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def extract_data(**context):
    pg_host = os.getenv('POSTGRES_ANALYTICS_HOST')
    pg_port = os.getenv('POSTGRES_PORT', '5432')
    pg_db = os.getenv('ANALYTICS_DB')
    pg_user = os.getenv('ETL_USER')
    pg_password = os.getenv('ETL_PASSWORD')

    conn_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
    engine = create_engine(conn_string)

    query = "SELECT * FROM homework.iris_processed"
    df = pd.read_sql(query, engine)

    context['ti'].xcom_push(key='iris_data', value=df.to_json())

def train_model(**context):
    iris_json = context['ti'].xcom_pull(key='iris_data', task_ids='extract_data')
    df = pd.read_json(iris_json)

    X = df.drop(columns=['species', 'is_species__setosa', 'is_species__versicolor', 'is_species__virginica', 'is_species__', 'species_label_encoded'], errors='ignore')
    y = df['species_label_encoded']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    clf = RandomForestClassifier()
    clf.fit(X_train, y_train)
    predictions = clf.predict(X_test)
    acc = accuracy_score(y_test, predictions)

    if acc < 0.8:
        raise AirflowFailException(f"Accuracy too low: {acc:.4f}")

    context['ti'].xcom_push(key='model_accuracy', value=acc)

with DAG(
    dag_id='process_iris_pipeline',
    default_args=default_args,
    description='Extract iris data from DB, train ML model, and notify by email',
    schedule_interval='0 1 22-24 4 *',
    catchup=True,
    tags=['iris', 'ml', 'db'],
) as dag:

    extract_data_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        provide_context=True,
    )

    train_model_task = PythonOperator(
        task_id='train_model',
        python_callable=train_model,
        provide_context=True,
    )

    notify_success = EmailOperator(
        task_id='notify_success',
        to='hnatenkoirina5@gmail.com',
        subject='Airflow Iris Pipeline Success',
        html_content="""
            <h3>Pipeline completed successfully!</h3>
            <p>Model accuracy exceeded threshold.</p>
        """,
    )

    extract_data_task >> train_model_task >> notify_success