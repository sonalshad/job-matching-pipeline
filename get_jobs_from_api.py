import requests
import pandas as pd
import numpy as np
import json
from google.cloud import storage
from datetime import date, datetime
import os
import time
from user_definition import *
from google.oauth2 import service_account
from google.cloud import aiplatform


#os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_API_KEY


json_creds = json.loads(GOOGLE_API_STRING.strip(),strict=False)
#json_creds = json.loads(json_string,strict=False)
project_id = json_creds['project_id']
credentials = service_account.Credentials.from_service_account_info(json_creds)
aiplatform.init(project=project_id, credentials=credentials)



api_1_fields = ['id','companyName','title','salary','jobUrl','location','postedTime','description']
api_2_fields = ['job_id','employer_name','job_title','salary','job_apply_link','location','job_posted_at_datetime_utc','job_description']


def write_data_to_gcs(bucket_name, folder_prefix, destination_file_name, json_data):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    blob = bucket.blob(folder_prefix + destination_file_name)
    blob.upload_from_string(json_data, content_type='application/json')
    print('Data written to GCS succesfully')
    print('Failed to write data to GCS')

def fetch_jobs_data_2(searchTitle):

    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {"query":f"{searchTitle} USA","page":"1","num_pages":"20","date_posted":"month"}

    headers = {
        "X-RapidAPI-Key": "ab34b8262amsh24f5a5da4139d42p1af943jsne9941931a106",
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    
    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
    except:
        print(f"Request failed")
        return


    folder_prefix = f"{datetime.now().strftime('%Y-%m-%d')}/"
    searchTitle = searchTitle.replace(" ", "")
    destination_file_name = f"{searchTitle}.json"

    bucket_name = GS_BUCKET_NAME
    json_data = json.dumps(data['data'])

    write_data_to_gcs(bucket_name,folder_prefix,destination_file_name,json_data)


def get_data():
    for searchTitle in ['Data Scientist','Data Analyst','Machine Learning Engineer']:
        time.sleep(5)
        fetch_jobs_data_2(searchTitle)
        print(f"Successfully searched jobs for {searchTitle}")

# def get_data():
#     folder_prefix = f"{datetime.now().strftime('%Y-%m-%d')}/"
#     searchTitle = 'data engineer'
#     searchTitle = searchTitle.replace(" ", "")
#     destination_file_name = f"{searchTitle}.json"

#     data = {
#         'data': {
#             'key1': 'value1',
#             'key2': 'value2',
#             'key3': 'value3',
#             'key4': 'value4',
#             'key5': 'value5'
#         }
#     }

#     bucket_name = GS_BUCKET_NAME
#     json_data = json.dumps(data['data'])
#     write_data_to_gcs(bucket_name, folder_prefix, destination_file_name, json_data)