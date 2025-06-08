from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

# Dossier de stockage des fichiers
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# URL de base (utilisée pour générer le lien de téléchargement)
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_url = f"{BASE_URL}/files/{file.filename}"
        return JSONResponse(content={"filename": file.filename, "url": file_url})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route pour servir les fichiers statiques
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")