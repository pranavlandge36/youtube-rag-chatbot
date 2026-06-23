from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
load_dotenv()
import os
index_name='youtube-chatbot'
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def create_index(video_id):
    existing_indexes = [i.name for i in pc.list_indexes()]

    if video_id not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )

    return pc.Index(video_id)