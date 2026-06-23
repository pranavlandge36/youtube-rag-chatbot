from langchain_openai import OpenAIEmbeddings
from langchain_core import documents
from langchain_pinecone import PineconeVectorStore
from models import embeddings
import os

index_name= 'youtube-chatbot'
def create_vector_stores(index, chunks):
    vector_store= PineconeVectorStore.from_documents(
        documents=chunks,
        embedding= embeddings,
        index_name=index_name
    )
    return vector_store

