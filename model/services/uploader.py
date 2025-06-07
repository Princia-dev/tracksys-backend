from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import shutil

app = FastAPI()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Sauvegarde locale
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Construire l’URL HTTPS à partir du domaine où ton backend est hébergé
        # Remplace "https://ton-domaine.com" par ton vrai domaine accessible en HTTPS
        base_url = "https://ton-domaine.com"
        file_url = f"{base_url}/files/{file.filename}"

        return JSONResponse(content={
            "filename": file.filename,
            "url": file_url
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Servir les fichiers statiques
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")