from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil

app = FastAPI()

# Dossier où on stocke les fichiers uploadés
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Chemin où enregistrer le fichier
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Sauvegarder le fichier sur le disque
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Retourner un lien (ici local, plus tard sera HTTPS)
        file_url = f"http://localhost:8000/files/{file.filename}"

        return JSONResponse(content={"filename": file.filename, "url": file_url})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Route pour servir les fichiers statiques uploadés (simple, pas sécurisé)
from fastapi.staticfiles import StaticFiles
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")