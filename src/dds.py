
from gcs_to_mongo import *
from get_jobs_from_api import get_data
from convert_to_embeddings import *
from airflow.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime
import os
import sys
sys.path.append('us-central1-job-recommender-40c669f7-bucket/utils')


# Define the DAG for the search engine pipeline
with DAG(
    dag_id="search_engine-airflow",
    start_date=datetime(2024, 2, 22),
    schedule_interval="@daily",
) as dag:

    os.environ["no_proxy"] = "*"

    # Define the PythonOperator for fetching products data
    get_jobs_op = PythonOperator(
        task_id="get_jobs_data", python_callable=get_data
    )

    gcs_to_mongo_op = PythonOperator(
        task_id="gcs_to_mongo", python_callable=gcs_to_mongodb_collection
    )

    summary_statistics_op = PythonOperator(
        task_id="summary_statistics", python_callable=calculate_summary_statistics
    )

    # convert_to_embeddings_op = PythonOperator(
    #     task_id="convert_to_embeddings", python_callable=embed_descriptions
    # )

    # Set the task dependencies
    # get_jobs_op >> gcs_to_mongo_op >> [summary_statistics_op, convert_to_embeddings_op]
    gcs_to_mongo_op >> summary_statistics_op
