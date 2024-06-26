from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime


default_args  = {
    'owner': 'Keenborder',
    'start_date': datetime(2024,5,24)
}

with DAG('spark_reddit_pipeline',
        default_args=default_args,
        catchup=True,
        schedule_interval='@hourly') as dag:
    
    start = PythonOperator(
    task_id="start",
    python_callable = lambda: print("Jobs started"))

    spark_job = SparkSubmitOperator(
        task_id = 'reddit_pipeline',
        application = '/opt/airflow/pipelines/reddit_pipeline.py',
        py_files='/opt/airflow/utils/constants.py',
        conn_id = 'spark-master',
        verbose = True
    )
    end = PythonOperator(
    task_id="end",
    python_callable = lambda: print("Jobs completed successfully"),
    dag=dag
)
    start >> spark_job >> end