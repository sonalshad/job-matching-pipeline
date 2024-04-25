import os
import json
import re
import time
import pandas as pd
from google.cloud import storage
from google.cloud import vision
import warnings
import pymongo
import certifi
from langchain_google_vertexai import VertexAI
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from user_definition import *
from google.oauth2 import service_account
from google.cloud import aiplatform

from io import BytesIO


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ['GOOGLE_API_KEY']

def generate_prompt(resume_text, job_description):
    prompt = f"""
                You are tasked with developing a tool to assist job seekers in matching their resumes to job descriptions effectively. 
                Your tool will compare the content of a resume to the job description of a specific job and provide concise insights into 
                the alignment between the two. Your task is to generate two concise bullet points summarizing the matching keywords, 
                skillsets or any other information found in both the resume and the job description. These bullet points should highlight 
                why the resume and the job listing are a good match based on the shared keywords and skillsets. Given below is the resume text 
                and the job description.

                Resume text:{resume_text}

                Job description:{job_description}

                """
    return prompt


# Function to upload file to Google Cloud Storage
def upload_to_gcs(file_contents, bucket_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(file_contents, content_type='application/pdf')
    return f'gs://{bucket_name}/{destination_blob_name}'


def get_matching_points(resume_text, job_descriptions):
    matching_points = []
    model = VertexAI(model_name="gemini-pro", project=GCP_PROJECT_NAME)
    for job_description in job_descriptions:
        prompt = generate_prompt(resume_text, job_description)
        points = model.invoke(prompt)
        matching_points.append(points)
        time.sleep(2)
    return matching_points


def parse_resume(resume, user_sample=True):

    if user_sample:
        with open('resume/Param_Mehta_Resume.txt', 'r') as file:
            file_contents = file.read()
        return file_contents

    file_contents = resume.read()
    file_name = resume.name

    # Specify your Google Cloud Storage bucket name and destination blob name
    gs_output_path = f'gs://{GS_BUCKET_NAME}/parsed_resume_txt/'
    destination_blob_name = f'uploaded_resume_pdf/{file_name}'

    gcs_url = upload_to_gcs(
        file_contents, GS_BUCKET_NAME, destination_blob_name)
    docs = async_detect_document(gcs_url, gs_output_path)

    return docs[0]


def find_jobs(title, resume_text):

    warnings.filterwarnings('ignore', category=UserWarning, message='TypedStorage is deprecated')
    embeddings_function = HuggingFaceInstructEmbeddings(
        model_name="hkunlp/instructor-base", model_kwargs={"device": 'cpu'})

    print(title)
    vector_search = MongoDBAtlasVectorSearch.from_connection_string(
        ATLAS_CONNECTION_STRING,
        f"{DB_NAME}.{JOBS_COLLECTION_NAME}",
        embeddings_function,
        index_name=VECTOR_INDEX_NAME)

    # Execute the similarity search with the given query
    results = vector_search.similarity_search_with_score(
        query=resume_text,
        k=3,
        pre_filter={"searchTitle": {"$eq": title}},
    )

    results_df = get_results_df(results, resume_text)

    return results_df

def get_stats_data():
    ca = certifi.where()
    client = pymongo.MongoClient(ATLAS_CONNECTION_STRING, tlsCAFile=ca)

    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    collection = client[DB_NAME][COLLECTION_NAME_STATS]
    stats = collection.find()

    data = list(stats)
    df = pd.DataFrame(data)
    
    return df.drop('_id', axis = 1)

def get_results_df(results, resume_text):
    job_descriptions = []
    job_details = []
    for doc, score in results:
        job_descriptions.append(doc.page_content)
        job_detail = doc.metadata
        job_detail['similarity_score'] = score
        job_details.append(job_detail)
    matching_points = get_matching_points(resume_text, job_descriptions)
    results_df = pd.DataFrame(job_details)
    results_df['matching_points'] = matching_points
    return results_df


def async_detect_document(gcs_source_uri, gcs_destination_uri):
    """
    Perform OCR on PDF/TIFF files stored on Google Cloud Storage asynchronously.

    Args:
        gcs_source_uri (str): The GCS URI of the source file.
        gcs_destination_uri (str): The GCS URI to store the output JSON file.

    Returns:
        list: List of extracted text from the document.
    """

    # Supported mime_types are: 'application/pdf' and 'image/tiff'
    mime_type = "application/pdf"

    # How many pages should be grouped into each json output file.
    batch_size = 1

    client = vision.ImageAnnotatorClient()
    feature = vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)

    # Set up input and output configurations
    gcs_source = vision.GcsSource(uri=gcs_source_uri)
    input_config = vision.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)
    gcs_destination = vision.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size
    )

    # Create an asynchronous request
    async_request = vision.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config, output_config=output_config
    )

    # Execute the asynchronous request
    operation = client.async_batch_annotate_files(requests=[async_request])

    print("Waiting for the operation to finish.")
    operation.result(timeout=420)

    # Access the result files stored on GCS
    storage_client = storage.Client()
    match = re.match(r"gs://([^/]+)/(.+)", gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)
    bucket = storage_client.get_bucket(bucket_name)

    # Extract text from each result file
    docs = []
    for filename in [blob for blob in list(bucket.list_blobs(prefix=prefix)) if not blob.name.endswith("/")]:
        json_string = filename.download_as_bytes().decode("utf-8")
        response = json.loads(json_string)
        response = response["responses"][0]
        annotation = response["fullTextAnnotation"]
        docs.append(annotation['text'])

    return docs