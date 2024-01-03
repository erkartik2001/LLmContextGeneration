import chromadb
from llama_index.vector_stores import ChromaVectorStore
from llama_index import SimpleDirectoryReader, StorageContext, VectorStoreIndex
from dotenv import load_dotenv
from chromadb.utils import embedding_functions
import os
import openai
import re


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
persist_dir = os.getenv("VECTOR_DB_DIR_PATH")
openai.api_key = openai_api_key

client = chromadb.PersistentClient(persist_dir)
embedding = "text-embedding-ada-002"

embedding_function = embedding_functions.OpenAIEmbeddingFunction(api_key=openai_api_key, model_name=embedding)


# if not any(collection.name == "web_collection" for collection in client.list_collections()):
#     collection = client.create_collection("web_collection", embedding_function=embedding_functions.OpenAIEmbeddingFunction(model_name=embedding,api_key=openai_api_key))
# else:
#     collection = client.get_collection("web_collection",embedding_function=embedding_functions.OpenAIEmbeddingFunction(model_name=embedding,api_key=openai_api_key))

if not any(collection.name == "web_collection" for collection in client.list_collections()):
    collection = client.create_collection("web_collection", embedding_function=embedding_function)
else:
    collection = client.get_collection("web_collection",embedding_function=embedding_function)

vec_store = ChromaVectorStore(chroma_collection=collection)
stcontext = StorageContext.from_defaults(vector_store=vec_store)
path = os.getenv("SCRAPPED_DATA_PATH")


def store_docs_embedding():
    """
    Pushes document embedding into the Vector DB

    Args:
        docs (document): A document containging chunks of data.

    Returns:
        Boolean
    """
    try:
        document = SimpleDirectoryReader(path).load_data()
        index = VectorStoreIndex.from_documents(documents=document,storage_context=stcontext)

        index._storage_context.persist(persist_dir)
    
    except Exception as e:
        print(f"Error storing doucment embeddding : {e}")
        return None

    return True


def query_docs(query,n_results=2):
    """
    Queries Vector DB 

    Args:
        query (string): Query which is used to perform semantic search

    Returns:
        context (string): A string containing results found after querying Vector DB.
    """
    context = ""
    results = collection.query(query_texts=[query],n_results=n_results)

    for i in range(n_results):
        result = results["documents"][0][i]
        context+=result + " "

    # context = context.replace("\n"," ")
    context = re.sub(r'\s+',' ', string=context)

    return context
    




