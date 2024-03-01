from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain.embeddings import HuggingFaceInstructEmbeddings
from io import BytesIO
import pymongo
from user_definition import *
import certifi

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

    
