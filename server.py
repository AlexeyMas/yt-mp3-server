from fastapi import FastAPI
import subprocess
import os
from fastapi.responses import FileResponse

app = FastAPI()
DOWNLOADS_FOLDER = "downloads"
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

@app.get("/")
def home():
    return {"message": "YouTube to MP3 Server is Running"}

@app.get("/download")
def download_audio(url: str):
    filename = os.path.join(DOWNLOADS_FOLDER, "audio.mp3")

    # Використовуємо yt-dlp для завантаження
    command = [
        "yt-dlp", "-x", "--audio-format", "mp3",
        "-o", filename, url
    ]
    subprocess.run(command, check=True)

    return FileResponse(filename, media_type="audio/mpeg", filename="audio.mp3")
