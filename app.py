import streamlit as st
import pandas as pd
from helper import *
#from langchain.vectorstores import MongoDBAtlasVectorSearch

st.set_page_config(layout="wide")


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = GOOGLE_API_KEY_FILE

# Streamlit App
st.title('Job Search')

# Dropdown for Job Title
st.subheader("Enter Job Title")
job_title_options = ['Software Engineer', 'Data Scientist', 'Product Manager', 'UX Designer', 'Business Analyst']
selected_job_title = st.selectbox('', job_title_options)

# Dropdown for Location
st.subheader("Enter location")
location_options = ['New York', 'San Francisco', 'Chicago', 'Los Angeles', 'Seattle']
selected_location = st.selectbox('', location_options)

# File uploader for PDF
st.subheader("Upload your resume")
resume = st.file_uploader("", type="pdf")

if resume is not None:
    # Submit Button
    if st.button('Find Jobs'):
        # Processing and display result
        st.write('Processing...')
        resume_text = parse_resume(resume)
        st.write(resume_text)
        st.write('Searching best jobs for you...')
        jobs_result = find_jobs(selected_job_title, selected_location,resume_text)
        st.write(jobs_result)
