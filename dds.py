
import sys
sys.path.append('us-central1-job-recommender-40c669f7-bucket/utils')

from get_jobs_from_api import get_data
from gcs_to_mongo import *
import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# Define the DAG for the search engine pipeline
with DAG(
    dag_id="search_engine-airflow",
    start_date=datetime(2024, 2, 22),
    schedule_interval="@daily",
) as dag:

    os.environ["no_proxy"] = "*"

    # Define the PythonOperator for fetching products data
    # get_jobs_op = PythonOperator(
    #     task_id="get_jobs_data", python_callable=get_data
    # )


    gcs_to_mongo_op = PythonOperator(
        task_id="gcs_to_mongo", python_callable=gcs_to_mongodb_collection
    )

    # Set the task dependencies
    # get_jobs_op >> gcs_to_mongo_op >> [aggg stattistics, embeddings]
    gcs_to_mongo_op