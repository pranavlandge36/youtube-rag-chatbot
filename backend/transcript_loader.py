from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api.proxies import WebshareProxyConfig
from urllib.parse import urlparse, parse_qs
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable
)
from faster_whisper import WhisperModel
import yt_dlp
import os
from dotenv import load_dotenv
import time
load_dotenv()

### EXTRACT VIDEO ID 
# vid_id= parse_qs(urlparse(url).query)["v"][0]
def get_video_id(url:str)->str:
    vid_id= parse_qs(urlparse(url).query)["v"][0]
    return vid_id


def get_youtube_transcript(url: str):

    vid_id = parse_qs(urlparse(url).query)["v"][0]

    api = YouTubeTranscriptApi(
        proxy_config=WebshareProxyConfig(
            proxy_username=os.getenv("WEBSHARE_USERNAME"),
            proxy_password=os.getenv("WEBSHARE_PASSWORD"),
        )
    )

    transcript_list = api.fetch(
        vid_id,
        languages=["en"]
    )

    transcript = "".join(
        chunk.text
        for chunk in transcript_list
    )

    return transcript, vid_id.lower()



def download_audio(url):

    for attempt in range(10):

        proxy = (
            f"http://{os.getenv('WEBSHARE_USERNAME')}:"
            f"{os.getenv('WEBSHARE_PASSWORD')}@p.webshare.io:80"
        )

        try:

            print(f"\nAttempt {attempt + 1}")

            ydl_opts = {
                "format": "bestaudio/best",
                "outtmpl": "audio.%(ext)s",
                "quiet": True,
                "proxy": proxy,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print(f"Success on attempt {attempt + 1}")

            for file in os.listdir():
                if file.startswith("audio."):
                    return file

        except Exception as e:

            print(f"Attempt {attempt + 1} failed")
            print(type(e).__name__)
            print(str(e))

            if attempt == 9:
                raise

            time.sleep(2)

    raise Exception("Could not download audio after 10 attempts")
    
    
model = WhisperModel(
        'tiny',
        device='cpu', compute_type='int8'
    )

def get_whisper_transcript(url: str):
    print("Downloading audio...")
    audio_file = download_audio(url)
    print("Audio downloaded:", audio_file)
    print("Starting Whisper transcription...")
    vid_id= parse_qs(urlparse(url).query)["v"][0]

    try:
        segments, _ = model.transcribe(audio_file)
        print("Whisper finished")
        transcript = " ".join(
            segment.text
            for segment in segments
        )

        return transcript,vid_id.lower()

    finally:
        if os.path.isfile(audio_file):
            os.remove(audio_file)

def get_transcript(url:str):
    try:
        print("Trying YouTube captions...")
        return get_youtube_transcript(url)
    except Exception as e:
        print(f"Caption fetch failed: {e}")
        return get_whisper_transcript(url)

