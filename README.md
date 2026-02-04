# PDF-to-MP3 Genie

Convert PDF documents into MP3 audio files.

https://pdf-to-mp3-genie.netlify.app/

---

## Stack

- React (frontend)
- FastAPI (backend)
- Python
- Text-to-Speech

---

## Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

---

### Frontend
```bash
cd frontend
npm install
npm start
```

---

API

POST /api/upload
Upload a PDF → receive an MP3.

---

License

MIT
