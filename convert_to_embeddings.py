from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain.embeddings import HuggingFaceInstructEmbeddings
from io import BytesIO
from pymongo.mongo_client import MongoClient
from user_definition import *

def embed_descriptions():
    embeddings_function = HuggingFaceInstructEmbeddings(
        model_name="hkunlp/instructor-large", model_kwargs={"device": 'cpu'}
    )

    client = MongoClient(ATLAS_CONNECTION_STRING)
                            
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

    vector_search = MongoDBAtlasVectorSearch.from_texts(
    descriptions,
    embeddings_function,
    metadatas,
    client[DB_NAME][JOBS_COLLECTION_NAME])

    collection.deleteMany({})

embed_descriptions()
