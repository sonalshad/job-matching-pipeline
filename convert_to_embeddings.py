from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain.embeddings import HuggingFaceInstructEmbeddings
from io import BytesIO
import pymongo
from user_definition import *
import certifi
from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, countDistinct, split


def embed_descriptions():
    embeddings_function = HuggingFaceInstructEmbeddings(
        model_name="hkunlp/instructor-large", model_kwargs={"device": 'cpu'}
    )

    ca = certifi.where()
    client = pymongo.MongoClient(ATLAS_CONNECTION_STRING, tlsCAFile=ca)

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    collection = client[DB_NAME][COLLECTION_NAME]
    new_jobs = collection.find()

    descriptions = []
    metadatas = []
    for job in new_jobs:
        descriptions.append(job['description'])
        metadatas.append(job)

    # deleting all the jobs from the new_jobs collection
    collection.deleteMany({})

    embeddings_collection = client[DB_NAME][JOBS_COLLECTION_NAME]

    # deleting all jobs from the jobs_data collection
    embeddings_collection.deleteMany({})

    vector_search = MongoDBAtlasVectorSearch.from_texts(
        descriptions,
        embeddings_function,
        metadatas,
        embeddings_collection)


def calculate_summary_statistics():
    # Initialize Spark session
    spark = SparkSession.builder.getOrCreate()
    conf = spark.sparkContext._jsc.hadoopConfiguration()
    conf.set("google.cloud.auth.service.account.json", GOOGLE_API_STRING)
    conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
    conf.set("fs.AbstractFileSystem.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")

    # Set up MongoDB connection
    ca = certifi.where()
    client = pymongo.MongoClient(ATLAS_CONNECTION_STRING, tlsCAFile=ca)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    # Explicitly project fields and exclude _id field
    pipeline = [{"$project": {"_id": 0}}]
    cursor = collection.aggregate(pipeline)

    # Load data into a Spark DataFrame
    df = spark.createDataFrame(cursor)

    # Split the salary column by hyphen and convert to numeric
    split_salary = split(df['salary'], ' - ')
    df = df.withColumn('min_salary', split_salary.getItem(0).cast("double"))
    df = df.withColumn('max_salary', split_salary.getItem(1).cast("double"))
    df = df.withColumn('average_salary', round((col('min_salary') + col('max_salary')) / 2, 2))

    # Aggregations
    job_title_aggregation = df.groupBy("searchTitle").agg(count("*").alias("total_jobs"))
    salary_aggregation = df.groupBy("searchTitle").agg(round(avg('average_salary'),2).alias("average_salary"))

    split_location = split(df['location'], ' - ')
    df = df.withColumn('city', split_location.getItem(0))
    df = df.withColumn('state', split_location.getItem(1))

    city_aggregation = df.agg(countDistinct("city").alias("city"))
    state_aggregation = df.agg(countDistinct("state").alias("state"))

    # Join all aggregations into a single DataFrame
    aggregated_df = job_title_aggregation.join(salary_aggregation, "searchTitle", "left")

    # Get the aggregated value from location_aggregation DataFrame
    distinct_job_city_value = city_aggregation.collect()[0]["city"]
    distinct_job_state_value = state_aggregation.collect()[0]["state"]

    # Add a new column to aggregated_df with the aggregated value from location_aggregation
    aggregated_df = aggregated_df.withColumn("city", lit(distinct_job_city_value))
    aggregated_df = aggregated_df.withColumn("state", lit(distinct_job_state_value))

    # Convert DataFrame to RDD and push to MongoDB
    # aggregated_rdd = aggregated_df.rdd
    collection_stats = db[COLLECTION_NAME_STATS]
    aggregated_df.show()
    aggregated_df = aggregated_df.rdd.map(lambda row: row.asDict())

    push_to_mongo(collection_stats, aggregated_df)

    # Stop SparkSession
    spark.stop()