from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.output_parsers import StructuredOutputParser
import pandas as pd
import sqlite3
import zipfile
import io

con = sqlite3.connect('eng_subtitles_database.db')

df = pd.read_sql_query('SELECT * FROM zipfiles', con)


def decode_method(binary_data):
    with io.BytesIO(binary_data) as f:
        with zipfile.ZipFile(f, 'r') as zip_file:
            subtitle_content = zip_file.read(zip_file.namelist()[0])
    
    return subtitle_content.decode('latin-1')

df['file_content'] = df['content'].apply(decode_method)

print(df.head()['file_content'][0])

# import os
# print(os.path.exists('dataset'))
# API_KEY = open('.genimi.txt').read().strip()

# embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)

# docs = DirectoryLoader(path="dataset", glob="**/*.srt", loader_cls=TextLoader, show_progress=True)
# docs = docs.load()
# print(len(docs))

# splitted_text = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
# chunks = splitted_text.split_documents(docs)

# db = Chroma(collection_name='subtitle_knowledge_base',
#             embedding_function=embeddings,
#             persist_directory='./chroma.db'
#             )
# batch_size = 100
# for i in range(0, len(chunks), batch_size):
#     batch = chunks[i:i + batch_size]
#     db.add_documents(batch)
#     print(f"✅ Processed batch {i // batch_size + 1}/{(len(chunks) // batch_size) + 1}")

# while True:
#     user_input=input('*User: ')

#     if user_input == 'q':
#         break

#     ai_response = db.similarity_search_with_relevance_scores(user_input, k=1)

#     print('\n\n *AI: '.join([doc.page_content for doc, _score in ai_response]))