from airflow import DAG
from airflow.providers.apache.spark.operators.spark.submit import SparkSubmitOperator
from datetime import datetime
import os
import sys


default_args  = {
    'owner': 'Keenborder',
    'start_date': datetime(2024,5,18)
}



with DAG('spark_reddit_pipeline',
        default_args=default_args,
        schedule_interval='@dialy') as dag:
    
    submit_job = SparkSubmitOperator(
        task_id = 'reddit_pipeline',
        application = '/opt/airflow/pipelines/reddit_pipeline.py',
        py_files='/opt/airflow/utils/constants.py',
        conn_id = 'spark-iceberg'
    )
    submit_job