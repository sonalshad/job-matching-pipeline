import os

ATLAS_CONNECTION_STRING = os.environ['ATLAS_CONNECTION_STRING']
DB_NAME = os.environ['DB_NAME']
COLLECTION_NAME = os.environ['COLLECTION_NAME']
VECTOR_INDEX_NAME = os.environ['VECTOR_INDEX_NAME']
GS_BUCKET_NAME = os.environ['GS_BUCKET_NAME']
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
GCP_PROJECT_NAME = os.environ['GCP_PROJECT_NAME']
MONGO_USERNAME = os.environ['MONGO_USERNAME']
MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
JOBS_COLLECTION_NAME = os.environ['JOBS_COLLECTION_NAME']
COLLECTION_NAME_STATS = os.environ['COLLECTION_NAME_STATS']
GOOGLE_API_KEY = "dds_project.json"
GOOGLE_API_STRING = """
{
  "type": "service_account",
  "project_id": "linkedin-job-recommender",
  "private_key_id": "2193b60dac9fc978aff7c0d493048de2358fbd1d",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCp3xzqovs28jRN\nTc6MtBa4KGgpJn7dlVAWqoccnoQNVc0UFTfelq4ZXIHBV4ujSev52BI/f1p4Ajwx\nqeRJui8/rvTIJsgTd9uLjj2LaGy+uEn/GFU4oB3sVMdBaVlYlTg4LEVvqP6w3o8F\nkEr3gUErG1qj+g+wmKv3w9gemeaS/lu5t4YYwNtMBD9tslvGh9/7QZXKq9Amhz3M\nmAZV/elesKZTVEuD4hiLeeWxgpqbShzRYSTdZp5cJe2GBnyHTZrepL6K6RhT2VV1\nWGNl8rxMqaKNRWuE19W/6C9Sd7rCj8JFnlymBkgKzNnAHYzyX4K7RAg2rjiKhOOw\nvJlr0mETAgMBAAECggEABCSTMaHB8LLIKxklBXIgRQ4vOXmyibg/g3NV55Ecyq/M\nrZsK3scxUyBaGxtbJiNXuaMsZsILXyE8KJXqdxCEYHrlhhAevGLQRuoJfuHlbQ1U\n41TLl0hIZ+AgGpdK0jSUHMKaUEErMlMV4okvWt6bIUWsgz1GWVnlL8i7TPEXRNRx\nv4GsvPmw7gJwNc8/hZpOzxbYtaRZXn8YkfT5yFo+FFP4HD67qC7BZ1xWpNKd8fdK\nuGtsGur1NLRVNGvHRdyT9SwQRVzooJ0v50bf88sJMpzq2902XiYGuGg228BVsAwQ\nFvlPxfr9XcfobpKnsr31FeqVEk1bPGYrB62CXp1UYQKBgQDSRNqgidkAVs0KAy9q\nVoFfqUkkvZaf5G2O7XuuEBwrDWqucFBGyRLSDUWqAia75rG9nLvxLbIs9b9wpM26\nZjQdyglITrn9A/U+xe2OxCFLvIC+M3yDgrmaryZp0WONuF7qfEbDzVA0Iw4+3b+G\nwho2F7lmL1wM0snxkm/8s9mJAwKBgQDO0Q0fAePdyDQGBTZv4vIYGEJB4kFkjPvh\noszxm1p+Ucym3Ib/TCzTXiiX9/q9PnX8e3g3vinFpgHPkLbAen8d3+iytbjMX3T0\n7Cfzb/RpMsOXSsVmG8nYA1A5XR37il09l+SjQ5SZyb/aLg8SZ4ewfxOhg2G6QIBc\n3he/4dLisQKBgAH4TywN3pCYP5eGbB1M7i1dQqgrdovM8hHSu8PntrvYhlVYDAh9\nvcVmBm8PUhmUkbm7DC+4Q+ET9FUz1hGW/4n/6JJa2nc6YEPUSuN5hu5Ut8gQZ2w7\n/00psuxu38XmIk2EGI2hEM1MPsfr/+1dSC2Vj1EbxHsCRo4S1yXA8ZrNAoGACKMg\naigZDR0cVxgGovuWYr04nynE018z8cNrzbdQOzBNXLafCLB0ussW5OndVePy5318\nks9lTTTWpIWFrFoxTt0YCcafFiHyb3whWwBU88PD+WCNB+unLVdOFWc3Jlcr97ON\nP+hFn3qWgZUk2f7q4ssb1cX34eBpu/cmhMP4m7ECgYANPglYXm816n7D+HhQBpcH\nfFydn2kLNl77FeBOooIMib5wh7DbQ9bxzyqXScSo81q9a6SZ65YJhqrrrt42Cmxz\nnoAEYZ0qk2mP0EuBwIynQ/BSbLyxZ/0EhmBDjguncyJTEK+fx8BD3mc2Gms01GOa\n+QNVeY84dATpkhcDLd8aSQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "shagun-dds@linkedin-job-recommender.iam.gserviceaccount.com",
  "client_id": "105296236148058281885",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/shagun-dds%40linkedin-job-recommender.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""