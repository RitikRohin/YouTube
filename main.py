from fastapi import FastAPI, Query
from fastapi.responses import FileResponse, JSONResponse
from yt_dlp import YoutubeDL
import os
import uuid

app = FastAPI()

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Function to download YouTube media
def download_media(url: str, format: str = "audio") -> str:
    file_id = str(uuid.uuid4())
    output_template = os.path.join(DOWNLOAD_DIR, f"{file_id}.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best" if format == "audio" else "bestvideo+bestaudio/best",
        "outtmpl": output_template,
        "merge_output_format": "mp4" if format == "video" else "mp3",
        "quiet": True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        ext = "mp4" if format == "video" else "mp3"
        filename = f"{file_id}.{ext}"
        return os.path.join(DOWNLOAD_DIR, filename)

@app.get("/")
async def root():
    return {"message": "YouTube Downloader API is running!"}

@app.get("/download")
async def download(url: str = Query(...), format: str = Query("audio")):
    try:
        filepath = download_media(url, format)
        return FileResponse(filepath, media_type="application/octet-stream", filename=os.path.basename(filepath))
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
