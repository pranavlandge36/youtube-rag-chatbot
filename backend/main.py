from cleanup import cleanup_old_vectors
from apscheduler.schedulers.background import BackgroundScheduler
from cleanup import cleanup_old_vectors

from transcript_loader import get_transcript,get_video_id
from chunking import make_chunks
from pinecone_utils import create_index
from embedding import create_vector_stores
from retriever import get_retriever
from prompt import prompts
from chains import build_chain
from video_exits import check_video_exists
from langchain_pinecone import PineconeVectorStore
from models import embeddings
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread

load_dotenv()


current_vid_id=None

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class URLRequest(BaseModel):
    url:str

class ChatRequest(BaseModel):
    query: str

processing_status = {}

def process_video(url):

    vid_id = get_video_id(url).lower()

    processing_status[vid_id] = "processing"

    try:

        index = create_index("youtube-chatbot")

        vector_store = PineconeVectorStore(
            index=index,
            embedding=embeddings
        )

        if not check_video_exists(index, vid_id):

            transcript, vid_id = get_transcript(url)

            chunks = make_chunks(
                transcript,
                vid_id
            )

            vector_store.add_documents(chunks)
            print("Video ID:", vid_id)
            print("Chunks created:", len(chunks))
            vector_store.add_documents(chunks)
            print("Documents added to Pinecone")
        processing_status[vid_id] = "ready"

        print("Processing Complete")

    except Exception as e:

        processing_status[vid_id] = f"error: {str(e)}"

        print(e)

# @app.post('/url')
# def put_url(req:URLRequest):
#     url= req.url
#     global current_vid_id
#     current_vid_id = get_video_id(url).lower()
#     vid_id= current_vid_id
#     index_name = "youtube-chatbot"

#     index = create_index(index_name)

#     vector_store = PineconeVectorStore(
#         index=index,
#         embedding=embeddings
#         )
#     if not check_video_exists(index, vid_id):

#         transcript, vid_id = get_transcript(url)

#         chunks = make_chunks(transcript, vid_id)
#         print("Video ID:", vid_id)
#         print("Chunks created:", len(chunks))
#         vector_store.add_documents(chunks)
#         print("Documents added to Pinecone")
#         return JSONResponse(
#             status_code=200,
#             content={"message": "Video indexed successfully"}
# )

#     else:
#         return JSONResponse(status_code=200,content=("Video already exists in Pinecone."))

@app.post('/url')
def put_url(req: URLRequest):

    global current_vid_id

    current_vid_id = get_video_id(req.url).lower()

    Thread(
        target=process_video,
        args=(req.url,),
        daemon=True
    ).start()

    return {
        "message": "Video processing started"
    }

@app.get("/status/{video_id}")
def get_status(video_id: str):

    return {
        "status":
        processing_status.get(
            video_id.lower(),
            "not_found"
        )
    }

@app.post('/chat')
def chat_user(req:ChatRequest):

    try:
        
        user_query=req.query
        global current_vid_id
        if current_vid_id is None:
            return JSONResponse(
        status_code=400,
        content={"error": "No video loaded. Call /url first."}
    )
        vid_id=current_vid_id
        if processing_status.get(vid_id) != "ready":
            return JSONResponse(
                status_code=400,
                content={
                    "error": "Video is still being processed. Please wait."
        }
    )
        user_query= user_query.strip()
        index = create_index("youtube-chatbot")
        vector_store = PineconeVectorStore(
        index=index,
        embedding=embeddings
        )
        retriever = get_retriever(
        vector_store,
        vid_id
        )

        chain = build_chain(
            retriever,
            prompts
        )
        docs = retriever.invoke(user_query)

        print("\nRetrieved Docs:\n")

        for i, doc in enumerate(docs):
            print(f"\n--- Doc {i+1} ---")
            print(doc.page_content[:500])
            print(doc.metadata)
        print("Query:", user_query)
        result= chain.invoke(user_query)

        return JSONResponse(status_code=200, content={'response':result})
    except Exception as e:
        return JSONResponse(status_code=500, content= str(e))

@app.delete("/cleanup")
def cleanup():

    index = create_index("youtube-chatbot")

    cleanup_old_vectors(index)

    return {"message": "cleanup complete"}

scheduler = BackgroundScheduler()

@app.on_event("startup")
def start_scheduler():

    index = create_index("youtube-chatbot")

    scheduler.add_job(
        lambda: cleanup_old_vectors(index),
        trigger="interval",
        hours=1
    )

    scheduler.start()

    print("Cleanup scheduler started")

@app.get('/')
def home():
    return {'message':'This is Youtube Chatbot'}

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "youtube-chatbot",
        "version": "1.0"
    }