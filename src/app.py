import streamlit as st
import pandas as pd
from helper import *
from PIL import Image
from user_definition import *
from google.oauth2 import service_account
from google.cloud import aiplatform

st.set_page_config(layout="wide")

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.environ['GOOGLE_API_KEY']


# Streamlit App
st.title('Job Search')
st.markdown('Job matching application designed for Data Science oriented people. Select your ideal job title, location, and upload your resume as a pdf.')
st.markdown('Using text matching, this app will output the 5 most optimal job listings for your criteria.')
st.subheader(':blue[Job Statistics]             :chart:')
stats_df = get_stats_data()
n = stats_df['total_jobs'].sum()
stats_df = stats_df.rename(columns={"searchTitle": "Job Title", "total_jobs": "Total Number of Jobs",
                                    'average_salary': 'Average Salary', 'city': 'Total Number of Cities', 'state': 'Total Number of States'})
st.write(stats_df)
st.subheader(":violet[Enter location]       :world_map:")
location_options = ['New York', 'San Francisco', 'Chicago', 'Los Angeles', 'Seattle']
button_clicked_ = {}
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
with col1:
    button_clicked_[location_options[0]] = st.button(location_options[0])   
with col2:
    button_clicked_[location_options[1]] = st.button(location_options[1])                               
with col3:
    button_clicked_[location_options[2]] = st.button(location_options[2])     
with col4:
    button_clicked_[location_options[3]] = st.button(location_options[3])
with col5:
    button_clicked_[location_options[4]] = st.button(location_options[4])   
selected_location = None
for location, is_clicked in button_clicked_.items():
    if is_clicked:
        selected_location = location
        break
if selected_location:
    st.write(f'Selected Location: {selected_location}')
else:
    st.write('No location selected')    
st.subheader(":blue[Enter Job Title]      :bar_chart:")
job_title_options = ['Data Scientist', 'Data Analyst', 'Machine Learning Engineer']
col1, col2, col3 = st.columns([1, 1, 1])

# Create buttons and store click states in the dictionary
button_clicked = {}
with col1:
    button_clicked[job_title_options[0]] = st.button(job_title_options[0])   
with col2:
    button_clicked[job_title_options[1]] = st.button(job_title_options[1])                               
with col3:
    button_clicked[job_title_options[2]] = st.button(job_title_options[2])          

# Determine the selected job title
selected_job_title = None
for job_title, is_clicked in button_clicked.items():
    if is_clicked:
        selected_job_title = job_title
        break
if selected_job_title:
    st.write(f'Selected Job Title: {selected_job_title}')
    st.session_state['selected_job_title'] = selected_job_title
else:
    st.write('No job title selected')


st.sidebar.image("usf_logo.png", use_column_width=True)
st.sidebar.image("job.png", use_column_width=True)
st.sidebar.write('[Github](https://github.com/sonalshad/job-matching-pipeline)')
# File uploader for PDF
st.subheader(":violet[Upload your resume]      :file_folder:")
resume = st.file_uploader("", type="pdf")

if resume is not None:
    # Submit Button
    if st.button(':rainbow[Find Jobs]'):
        # Processing and display result
        st.write('Processing ...')
        resume_text = parse_resume(resume)
        #st.write(resume_text)
        with st.spinner('Searching best jobs for you ...'):
            jobs_result = find_jobs(st.session_state['selected_job_title'], resume_text)

        for i, row in jobs_result.iterrows():
            st.markdown(f"## {row['companyName']}")
            st.markdown(f"### {row['title']}")
            st.write(f"Similarity Score: {round(row['similarity_score'],2)}")
            st.write(f"Location: {row['location']}")
            st.write(f"Salary: {row['salary']}")
            st.write(f"Job URL: {row['jobUrl']}")
            st.write(f"Matching Points:")
            st.write(f"{row['matching_points']}")
            st.markdown("---")
footer_text = """
---
[Github](https://github.com/sonalshad/job-matching-pipeline)
"""
st.markdown(footer_text)
