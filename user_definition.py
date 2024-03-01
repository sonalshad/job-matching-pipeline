import os

# ATLAS_CONNECTION_STRING = os.environ['ATLAS_CONNECTION_STRING']
# DB_NAME = os.environ['DB_NAME']
# COLLECTION_NAME = os.environ['COLLECTION_NAME']
# VECTOR_INDEX_NAME = os.environ['VECTOR_INDEX_NAME']
GS_BUCKET_NAME = os.environ['GS_BUCKET_NAME']
#GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']
GCP_PROJECT_NAME = os.environ['GCP_PROJECT_NAME']
# MONGO_USERNAME = os.environ['MONGO_USERNAME']
# MONGO_PASSWORD = os.environ['MONGO_PASSWORD']
# JOBS_COLLECTION_NAME = os.environ['JOBS_COLLECTION_NAME']
#GOOGLE_API_KEY = "dds_project.json"
GOOGLE_API_STRING = """
{
  "type": "service_account",
  "project_id": "linkedin-job-recommender",
  "private_key_id": "c90863b86da3ea2258da419c517e3bf933c5b0d8",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC5RYhtNJVRNX8P\nWRygNDyGCcTB+nRQvoIFjHRXZpXk6bToLro2lK3Zqat/pN7ve6mvaXFieuG21pcj\nKRyXh3kxeKZNEx6etveK5utwdPIpjh1Kjf9TtYeL9lvgV9W+sWlOdRVaxTvBaTUQ\nFMX31k/PpVFlcueDZmFemmYJbifuYbgVxa20qqXO8PrrfPDkFSQjKcqvFVtNs4kb\nCA1DjacwObwNiXAcYmDQ0luurct9TLAAcwFV1MZ6CtHfYfpDXyTbYTp/DV07YqgP\ndiSG4NXqMhCfJywh9Ucz9NrNkZO2IKrhvq6TGKT0F90AIiPdkX3hM6g/atkYteRQ\nXeaaD4A9AgMBAAECggEAD+H2W1hL6amSoivzQIeh3aLGP5PbN1XRmyyqh5iXhoeD\ndvkUhRvTWIrLVTa61uBs0EkTi4v5wB0e2UiLtzDJsrRDW22lbRlF2N5JdjtMTEQu\n3iaUqiYwf87nmvCktgOLAcsXQNASOpcskZuaShARCP3E39PNJY5YEA5f63SKT0zj\nEqk2YLtuq60XTfjbw/5OdBzzE+jMjCyRZgw2HP0bbapdUbKVVjwyPPmVOd3bLgmC\nABgpQB61yIoWeXzEnWfiNz2LSB6h7xRVu/cr8Q1HY/6zKzv87AUnHtKQMQSCP8EQ\nq3+9PkunuhMTR6x4KUI3lp4Ea5UqO8oEvxsYh+CD4QKBgQD6GF/Vy4bvzZ05/Xxi\n8paecji6qCX4lq4k5/4bH4Adlbz9B3FS0JLhk1jFNMq7RePLRX9nMr9LzXy9dkjt\ndD98rck9ZIKGJCtK6cOXgrUUDOFYT5qE8HDIlc9SlIjFDGWl8DXQaXqaATM4dKQX\nEdnv+1PR1qKOnMRN28ztGUjcnQKBgQC9pVoKQ2/PbQtODjLHqL7C0kQb5Fs1Jn4U\nmiBeSDjaANZlx8ap/SDYNf+5bWjakU1wOayPiqU1oWic1MI+F4oGVYsGMq9KVvZC\nQto7QtYtC6m5q1iQdKqvCFROBSvheyjNWa3sr2Fe80RE6eqG4QB0g5Kf5YyNGnp3\nOchAR4JQIQKBgQDaZhSysASLP4SQ0qMgCXassVSG9DYMixFSW2GVMAICU/PxBuHY\njxnlcXYw6PQtbFAMAAnNBgz11mGbVkNDUaPrbhvxx+cP22APEGrk0ZjuBH15UDLA\n6vOixuiA1gNGCJhvu4BTGvmcqXWgVIPDPayTHGhLM+NLJO1sjIi9eLofJQKBgQCE\nVTSOQt5rjHi9/9RZVBvA0H5sRB2M6g5CjAYYJCdfoAP7Q7sR9SsNFCkcmAb5tTin\nHeeWxjVgRgA8p43fTAepQdnf+lAs/J+cPxAPGCVhi2jkwXbsXiyYNKS3SI6FKa6g\nFHrz1LGKUxAJUnyvn6P0qbcP0lsQPzDDr1NX305EYQKBgE0EHDzMckUSEM2hjMgW\nlwc5PZIaCyLRLZrkEbSvYb26a3Zi0mPv1gdmv0tjz3Qm/GdGZtxFlUVyspXqK6iq\nH3lmfdEFe/m67xB1sKO7Bp/UgMFXiTwlFlt73lLPVWS9igPiqkTynNHShz5/zzzl\nfc12uCpgIRmoYdBa37yCwAki\n-----END PRIVATE KEY-----\n",
  "client_email": "dds-project@linkedin-job-recommender.iam.gserviceaccount.com",
  "client_id": "114768692486091169378",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dds-project%40linkedin-job-recommender.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}
"""


# api_1_fields = ['id','companyName','title','salary','jobUrl','location','postedTime','description']
# api_2_fields = ['job_id','employer_name','job_title','salary','job_apply_link','location','job_posted_at_datetime_utc','job_description']
