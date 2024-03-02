# Job Matching Pipeline #

## Executive Summary ## 
This repository contains a job matching pipeline using Google Cloud Storage (GCS), Airflow, PySpark, MongoDB, LLM packages on Python, Streamlit, and Google Vision OCR. The pipeline fetches job listing data from the JSearch API from RapidAPI, stores the data in GCS, cleans the data with PySpark, and loads the cleaned data into MongoDB where additional transformations are applied to calculate aggregated statistics and Langchain is used to create embeddings for automated job matching. When resumes are uploaded, Google Vision OCR parses out the relevant content and Langchain is used to transform it into embeddings that can be compared to the records in MongoDB. Based on cosine similarity, the top five jobs are displayed on the Streamlit user interface. We then used an LLM summarizer to synthesize the job descriptions of the top five roles.

## 1.0 Dataset and Goals ## 

### 1.1 Goal ###
Problem - Search tools on traditional job aggregation portals (e.g., LinkedIn, Ziprecruiter, and Indeed) are not very useful for leading edge fields such as Data Science, where responsibilities are not uniformly defined across the industry. As a result, job searchers from these disciplines have to spend time searching multiple job titles and reading through individual job descriptions to understand if it is a fit for their profile. 

Solution - We look to reduce time spent searching for the right fit by matching a user’s resume to open roles based on broad filters such as approximate job title and location. For this implementation, we have focused on a limited set of job titles (Data Scientist, Data Analyst, Machine Learning Engineer) and locations (By state: CA, IL, TX).  

Technical Skills - Through this project, we hope to showcase our understanding of 
How various technologies come together to form an automated data pipeline 
How to make decisions on data processing and storage based on a realistic data processing scenario where data can come from multiple sources and needs to be aggregated and processed at various speeds depending on the use case
How to implement a machine learning model with industry standard leading edge solutions such as OCR and Langchain 

### 1.2 Dataset ###
We used two sources of data:

JSearch from RapidAPI (Source): A real-time job posting database that scrapes from LinkedIn, Indeed, Glassdoor, and Google for Jobs. The output is in JSON with more than 30 data points per job, including job title, location, employer, employment type, category, industry/company type, job requirements, date posted, etc. 

Resumes uploaded in PDF format as the Google Vision OCR software is able to parse content from that document type
