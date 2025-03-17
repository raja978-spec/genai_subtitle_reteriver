from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.output_parsers import StructuredOutputParser


def load_data_to_chroma_db_batch_by_batch(db, data):
     batch_size = 100  
     for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        db.add_documents(batch)
        print(f"✅ Processed batch {i // batch_size + 1}/{(len(data) // batch_size) + 1}")

def subtitle_finder(user_input, load_new_data_to_model):
    API_KEY = open('.genimi.txt').read().strip()
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=API_KEY)
    docs = DirectoryLoader(path="dataset", glob="**/*.srt", loader_cls=TextLoader, show_progress=True)
    docs = docs.load()
    
    splitted_text = RecursiveCharacterTextSplitter(chunk_size=50, chunk_overlap=10)
    chunks = splitted_text.split_documents(docs)
    
    db = Chroma(collection_name='subtitle_knowledge_base',
            embedding_function=embeddings,
            persist_directory='./chroma.db'
            )
    if(load_new_data_to_model):
        print('Loading New Data To Vector DB By Batch.....')
        load_data_to_chroma_db_batch_by_batch(db, chunks)
        print('New Data Loaded')
    else:
        print('Model Uses Existing Vector DB Data')
    ai_response = db.similarity_search_with_relevance_scores(user_input, k=3)
    return ai_response