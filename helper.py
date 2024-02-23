import os
import json
import re
import pandas as pd
from google.cloud import storage
from google.cloud import vision
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings

from io import BytesIO

GOOGLE_API_KEY_FILE = "/Users/parammehta/Desktop/usf/dds/final_project/config/google_api.json"
#storage_client = storage.Client(project='your-project-id')


# Function to upload file to Google Cloud Storage
def upload_to_gcs(file_contents, bucket_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(file_contents, content_type='application/pdf')
    return f'gs://{bucket_name}/{destination_blob_name}'


def parse_resume(resume):
    
    file_contents = resume.read()
    file_name = resume.name
        
    # Specify your Google Cloud Storage bucket name and destination blob name
    bucket_name = 'truckx_demo'
    gs_output_path = 'gs://truckx_demo/parsed_resume_output/'
    destination_blob_name = f'uploads/{file_name}'
    
    gcs_url = upload_to_gcs(file_contents, bucket_name, destination_blob_name)
    docs = async_detect_document(gcs_url, gs_output_path)

    for i, text in enumerate(docs):
        txt_filename = f'parsed_resume_docs/{file_name.replace(".pdf", ".txt")}'
        with open(txt_filename, "w") as file:
            file.write(text)
    return 'Resume parsed successfully'
    
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
    input_config = vision.InputConfig(gcs_source=gcs_source, mime_type=mime_type)
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


def find_jobs(job_title, location, resume_text):

    embeddings_function = HuggingFaceInstructEmbeddings(
        model_name="hkunlp/instructor-large", model_kwargs={"device": 'cpu'}
    )

    vector_search = Chroma(persist_directory='db', embedding_function=embeddings_function)

        
    # Execute the similarity search with the given query
    results = vector_search.similarity_search_with_score(
        query=resume_text,
        k=5
    )

    rows = [(list(doc.metadata.values())[0],score) for doc, score in results]
    results_df = pd.DataFrame(rows,columns=['Job Url','Similarity Score']).round(4)

    for doc,score in results:
        print(doc.page_content)

    return results_df

# def find_jobs(job_title, location, resume_text):
#     # Simulated job data
#     mongo_db_query = get_specified_jobs(job_title,location)
#     # for job in mongo_db_query:
    
#     #         content = job['embedding']
#     #         docs.append(Document(page_content=content))
#     # print(len(docs))



#     vector_search = MongoDBAtlasVectorSearch.from_connection_string(
#     ATLAS_CONNECTION_STRING,
#     f"{DB_NAME}.{COLLECTION_NAME}",
#     OpenAIEmbeddings(),
#     index_name="default")

        
#     # Execute the similarity search with the given query
#     results = vector_search.similarity_search_with_score(
#         query=query,
#         k=top_k,
#         pre_filter={
#                 "$and": [
#                     {"job_title": {"$eq": job_title}},
#                     {"location": {"$eq": location}},
#                 ]
#             },
#     )
    
#     return results

#results is a list of tuple. (doc,score)