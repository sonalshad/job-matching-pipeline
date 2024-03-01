
import sys
sys.path.append('us-central1-job-recommender-40c669f7-bucket/utils')

from get_jobs_from_api import get_data
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

    Define the PythonOperator for fetching products data
    get_jobs_op = PythonOperator(
        task_id="get_jobs_data", python_callable=get_data
    )

    # Define the SparkSubmitOperator for moving data from GCS to MongoDB
    gcs_to_mongo_op = SparkSubmitOperator(
        task_id="gcs_to_mongo_data",
        packages="com.google.cloud.bigdataoss:gcs-connector:hadoop2-1.9.17,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1",
        exclude_packages="javax.jms:jms,com.sun.jdmk:jmxtools,com.sun.jmx:jmxri",
        conf={
            "spark.driver.userClassPathFirst": True,
            "spark.executor.userClassPathFirst": True,
        },
        verbose=True,
        application="gcs_to_mongo.py",
    )

    # Set the task dependencies
    get_jobs_op >> gcs_to_mongo_op >> [aggg stattistics, embeddings]