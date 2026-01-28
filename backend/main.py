from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
from gtts import gTTS
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

def cleanup_files(pdf_path: str, mp3_path: str):
    """Delete files after response is sent"""
    try:
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        if os.path.exists(mp3_path):
            os.remove(mp3_path)
    except Exception as e:
        print(f"Cleanup error: {e}")

@app.post("/upload")
async def upload_pdf(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    pdf_path = f"{UPLOAD_DIR}/{uuid.uuid4()}.pdf"
    mp3_path = f"{OUTPUT_DIR}/{uuid.uuid4()}.mp3"

    # Save PDF
    with open(pdf_path, "wb") as f:
        f.write(await file.read())

    # Read PDF
    text = ""
    with open(pdf_path, "rb") as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted.replace("\n", " ")

    if not text.strip():
        os.remove(pdf_path)  # Clean up immediately if error
        raise HTTPException(status_code=400, detail="No text found in PDF")

    # Text to speech using gTTS
    tts = gTTS(text=text, lang='en')
    tts.save(mp3_path)

    # Schedule cleanup after response is sent
    background_tasks.add_task(cleanup_files, pdf_path, mp3_path)

    return FileResponse(
        mp3_path,
        media_type="audio/mpeg",
        filename="output.mp3"
    )

@app.get("/")
async def root():
    return {"message": "PDF to Audio API is running"}