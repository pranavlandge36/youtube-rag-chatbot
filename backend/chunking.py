from langchain_text_splitters import RecursiveCharacterTextSplitter
import time


splitter = RecursiveCharacterTextSplitter(
    chunk_size= 500,
    chunk_overlap=100
)

def make_chunks(transcript, vid_id):
    chunks = splitter.create_documents(
    [transcript],
    metadatas=[{
        "video_id": vid_id.lower(),
        'created_at':time.time()
    }]
    )
    return chunks

