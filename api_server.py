from fastapi import FastAPI, Query
from pydantic import BaseModel
import yt_dlp
import json
import os

app = FastAPI()

KEY_FILE = "apikeys.json"

class YouTubeData(BaseModel):
    title: str
    thumbnail: str
    duration: str
    direct_url: str

def load_keys():
    if not os.path.exists(KEY_FILE):
        return []
    with open(KEY_FILE, "r") as f:
        return json.load(f).values()

def extract_info(url: str, format_code: str):
    ydl_opts = {
        "quiet": True,
        "skip_download": True,
        "simulate": True,
        "forcejson": True,
        "format": format_code,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            "title": info.get("title"),
            "thumbnail": info.get("thumbnail"),
            "duration": f"{int(info['duration']//60)}:{int(info['duration']%60):02}",
            "direct_url": info.get("url"),
        }

@app.get("/")
def home():
    return {"message": "✅ YouTube API Server is Live!"}

@app.get("/video", response_model=YouTubeData)
def get_video(url: str = Query(...), apikey: str = Query(...)):
    if apikey not in load_keys():
        return {"error": "❌ Invalid API Key"}
    return extract_info(url, "18")  # mp4 360p

@app.get("/audio", response_model=YouTubeData)
def get_audio(url: str = Query(...), apikey: str = Query(...)):
    if apikey not in load_keys():
        return {"error": "❌ Invalid API Key"}
    return extract_info(url, "140")  # m4a audio
