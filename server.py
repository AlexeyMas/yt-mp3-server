from fastapi import FastAPI, HTTPException
import subprocess
import os
from fastapi.responses import FileResponse

app = FastAPI()
DOWNLOADS_FOLDER = "downloads"
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

COOKIES_FILE = "cookies.txt"  # Файл cookies, збережений з браузера

@app.get("/")
def home():
    return {"message": "YouTube to MP3 Server is Running"}

@app.get("/download")
def download_audio(url: str):
    try:
        clean_url = url.split("?")[0]  # Видаляємо зайві параметри
        filename = os.path.join(DOWNLOADS_FOLDER, "audio.mp3")

        # Логування URL перед завантаженням
        print(f"Downloading audio from: {clean_url}")

        command = [
            "yt-dlp", "-x", "--audio-format", "mp3",
            "--cookies", COOKIES_FILE,  # Використовуємо cookies.txt
            "-o", filename, clean_url
        ]
        result = subprocess.run(command, capture_output=True, text=True)

        # Перевіряємо, чи не було помилки
        if result.returncode != 0:
            print("yt-dlp error:", result.stderr)
            raise HTTPException(status_code=500, detail="yt-dlp failed to process the URL")

        # Перевіряємо розмір файлу
        if os.path.exists(filename) and os.path.getsize(filename) > 1000:
            print(f"File downloaded successfully: {filename}")
            return FileResponse(filename, media_type="audio/mpeg", filename="audio.mp3")
        else:
            print("Downloaded file is empty")
            raise HTTPException(status_code=500, detail="Downloaded file is empty")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
