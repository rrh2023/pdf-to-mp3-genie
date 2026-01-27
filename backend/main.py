from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import boto3
import uuid
import os
import io

app = FastAPI()

# Lambda can only write to /tmp
TEMP_DIR = "/tmp"

# Initialize AWS Polly client
polly_client = boto3.client('polly')

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "https://YOUR-VERCEL-APP.vercel.app"
    ],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def read_root():
    return {"message": "PDF to Speech API", "status": "healthy"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    pdf_path = f"{TEMP_DIR}/{uuid.uuid4()}.pdf"
    mp3_path = f"{TEMP_DIR}/{uuid.uuid4()}.mp3"
    
    try:
        # Save uploaded PDF to /tmp
        with open(pdf_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Extract text from PDF
        text = ""
        with open(pdf_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted.replace("\n", " ") + " "
        
        if not text.strip():
            raise HTTPException(status_code=400, detail="No text found in PDF")
        
        # Limit text length (Polly has a 3000 character limit per request)
        # For longer texts, you'd need to split and concatenate audio
        if len(text) > 3000:
            text = text[:3000]
        
        # Convert text to speech using AWS Polly
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Joanna',  # Options: Joanna, Matthew, Amy, Brian, etc.
            Engine='neural'     # Neural voices sound more natural
        )
        
        # Get audio stream from Polly
        audio_stream = response['AudioStream'].read()
        
        # Clean up PDF file
        if os.path.exists(pdf_path):
            os.remove(pdf_path)
        
        # Return audio as streaming response
        return StreamingResponse(
            io.BytesIO(audio_stream),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=output.mp3"
            }
        )
        
    except Exception as e:
        # Clean up files on error
        for path in [pdf_path, mp3_path]:
            if os.path.exists(path):
                os.remove(path)
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

