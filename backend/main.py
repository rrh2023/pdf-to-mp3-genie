from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
from gtts import gTTS  # Changed from pyttsx3
import uuid
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_path = f"{UPLOAD_DIR}/{uuid.uuid4()}.pdf"
    mp3_path = f"{OUTPUT_DIR}/{uuid.uuid4()}.mp3"

    try:
        # Save PDF
        with open(pdf_path, "wb") as f:
            f.write(await file.read())

        # Read PDF
        reader = PyPDF2.PdfReader(open(pdf_path, "rb"))
        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted.replace("\n", " ")

        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in PDF")

        # Text to speech using gTTS
        tts = gTTS(text=text, lang='en')
        tts.save(mp3_path)

        return FileResponse(
            mp3_path,
            media_type="audio/mpeg",
            filename="output.mp3"
        )
    
    finally:
        # Cleanup files after response is sent
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        # Note: mp3_path will be cleaned up by FileResponse's background task

@app.get("/")
async def root():
    return {"message": "PDF to Audio API is running"}