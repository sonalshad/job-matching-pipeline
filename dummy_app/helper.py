import os
import json
import re
import pandas as pd
  

def find_jobs(job_title, location):
    """
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
    [companyName','title','salary','jobUrl','location','postedTime','similarity_score','matching_points']        
    """
    results_df = pd.DataFrame({'companyName': ['Amazon', 'Facebook'], 'title': ['Data Scientist', 'Data Analyst'],
                               'salary':[100, 2000], 'jobUrl':['link1', 'link2'],
                               'location':['SF', 'NY'],'postedTime':['3PM', '4PM'], 'similarity_score':[0.1,0.9], 'matching_points':[1,2]})
    n = 300
    return results_df, n
