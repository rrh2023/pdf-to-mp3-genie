from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import PyPDF2
import pyttsx3
import uuid
import os

app = FastAPI()
handler = Mangum(app)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    pdf_path = f"{UPLOAD_DIR}/{uuid.uuid4()}.pdf"
    mp3_path = f"{OUTPUT_DIR}/{uuid.uuid4()}.mp3"

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

    # Text to speech
    engine = pyttsx3.init()
    engine.save_to_file(text, mp3_path)
    engine.runAndWait()
    engine.stop()

    return FileResponse(
        mp3_path,
        media_type="audio/mpeg",
        filename="output.mp3"
    )
