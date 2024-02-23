import os
import json
from langchain.schema.document import Document
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceInstructEmbeddings


docs_path = 'data'
def convert_docs_to_embedding():

    docs = []
    for filename in os.listdir(docs_path):
        file_path = os.path.join(docs_path, filename)
        with open(file_path, 'r') as file:
            data = json.load(file)
            for i in range(len(data)):
                job = data[str(i)]
                desc = job['description']
                if desc.strip() == '':
                    continue
                metadata = {'jobUrl':job['jobUrl']}
                docs.append(Document(page_content=desc, metadata=metadata))

    embeddings_function = HuggingFaceInstructEmbeddings(
        model_name="hkunlp/instructor-large", model_kwargs={"device": 'cpu'}
    )

    vector_search =  Chroma.from_documents(docs, embeddings_function, persist_directory='db')
    print(docs[0])
    print(docs[1])
    print(len(docs))
    return


convert_docs_to_embedding()