import os
from datetime import date
from datetime import datetime
import pymongo
from google.cloud import storage
import json
from pyspark.sql import SparkSession
from user_definition import *
from google.oauth2 import service_account
from google.cloud import aiplatform
import certifi

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ.get('GOOGLE_API_KEY')

api_1_fields = ['id', 'companyName', 'title', 'salary',
                'jobUrl', 'location', 'postedTime', 'description']
api_2_fields = ['job_id', 'employer_name', 'job_title', 'salary',
                'job_apply_link', 'location', 'job_posted_at_datetime_utc', 'job_description']

json_creds = json.loads(GOOGLE_API_STRING.strip(), strict=False)
# json_creds = json.loads(json_string,strict=False)
project_id = json_creds['project_id']
credentials = service_account.Credentials.from_service_account_info(json_creds)
aiplatform.init(project=project_id, credentials=credentials)


def clean_job_data_spark(df, searchTitle):
    def clean_job(row):
        job = row.asDict()
        # Skipping jobs with missing fields
        if job['job_description'].strip() == '' \
                or job['job_title'].strip() == '' \
                or job['job_apply_link'].strip() == '' \
                or job['employer_name'].strip() == '':
            return None

        # Combining location fields into one
        location_parts = [job['job_city'],
                          job['job_state'], job['job_country']]
        job['location'] = ' - '.join(filter(None, location_parts))

        # Combining salary fields into one
        salary_parts = [str(job['job_min_salary']), str(job['job_max_salary'])]
        job['salary'] = ' - '.join(filter(None, salary_parts))

        api_1_fields = ['id', 'companyName', 'title', 'salary',
                        'jobUrl', 'location', 'postedTime', 'description']
        api_2_fields = ['job_id', 'employer_name', 'job_title', 'salary',
                        'job_apply_link', 'location', 'job_posted_at_datetime_utc', 'job_description']

        # Standardizing field names across different APIs
        for key1, key2 in zip(api_1_fields, api_2_fields):
            job[key1] = job[key2]

        # Removing unwanted fields and adding searchTitle
        cleaned_job = {key: job[key] for key in api_1_fields if key in job}
        cleaned_job['searchTitle'] = searchTitle
        return cleaned_job

    cleaned_jobs_rdd = df.rdd.map(clean_job).filter(lambda x: x is not None)

    return cleaned_jobs_rdd


def clean_data(spark, bucket_name, blob_name, searchTitle):
    """
    This function pulls the data from GCS bucket and maps the data into rdd.
    It takes the spark context, bucket name and file path for the GCS as inputs and returns an rdd.
    """
    # df = spark.read.option("multiline", "true").json(f"gs://{bucket_name}/{blob_name}")

    gcs_path = f"gs://{bucket_name}/{blob_name}"
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Read the JSON file from Google Cloud Storage
    with open("/tmp/temp_file.json", "wb") as file:
        blob = bucket.blob(blob_name)
        blob.download_to_file(file)

    # Convert the JSON file to a Spark DataFrame
    df = spark.read.json("/tmp/temp_file.json")

    try:
        cleaned_jobs_rdd = clean_job_data_spark(df, searchTitle)
        print("RDD created successfully!")
        return cleaned_jobs_rdd
    except Exception as e:
        print(e)


def push_to_mongo(mongo_collection, input_data):
    """
    This function pushes rdd data into MongoDB.
    """
    try:
        mongo_collection.delete_many({})
        mongo_collection.insert_many(input_data.collect(), ordered=False)
        print("Documents inserted to Mongo successfully!")
    except Exception as e:
        print(e)


def gcs_to_mongodb_collection():
    # Initialize Spark session
    spark_session = SparkSession.builder.getOrCreate()
    conf = spark_session.sparkContext._jsc.hadoopConfiguration()
    conf.set(
        "google.cloud.auth.service.account.json",
        GOOGLE_API_STRING,
    )
    conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    conf.set(
        "fs.AbstractFileSystem.gs.impl",
        "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem",
    )

    # Set up MongoDB connection
    ca = certifi.where()
    client = pymongo.MongoClient(ATLAS_CONNECTION_STRING, tlsCAFile=ca)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Clean data and create RDD

    folder_prefix = f"{datetime.now().strftime('%Y-%m-%d')}/"

    for searchTitle in ['Data Scientist', 'Data Analyst', 'Machine Learning Engineer']:
        blob_name = folder_prefix + searchTitle.replace(" ", "") + '.json'
        input_rdd = clean_data(
            spark_session, GS_BUCKET_NAME, blob_name, searchTitle)
        # function to preprocess text data here
        # clean input_rdd and return another rdd and store it as input_rdd
        push_to_mongo(collection, input_rdd)
