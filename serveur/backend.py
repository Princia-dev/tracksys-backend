from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import shutil
import psycopg2
from psycopg2.extras import RealDictCursor

# === CONFIGURATION DE L'APPLICATION ===
app = FastAPI()

# ✅ Autoriser les requêtes Cross-Origin (ex: depuis Netlify)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Ou ["https://trackerethique.netlify.app"] pour plus de sécurité
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === CONFIG UPLOAD FICHIERS ===
UPLOAD_DIR = os.path.abspath("uploaded_files")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ URL du backend (Render)
BASE_URL = os.getenv("BASE_URL", "https://tracksys-backend.onrender.com")

# === CONFIGURATION DE LA BASE POSTGRESQL ===
DB_CONFIG = {
    "host": "dpg-d1e12ofdiees73c2sfu0-a",         # ton host Render PostgreSQL
    "dbname": "tracksys_bd",
    "user": "postgres",                           # ✅ corrigé ici
    "password": "kSdrZm4De8otlWEQTPGe76EyAweHieoN",  # ⚠ À sécuriser dans une variable d’environnement plus tard
    "port": 5432
}

# === ROUTE POUR L’UPLOAD DE FICHIERS (ex: .zip/.exe) ===
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

# === SERVIR LES FICHIERS STATIQUES ===
app.mount("/files", StaticFiles(directory=UPLOAD_DIR), name="files")

# === MODÈLE POUR LES DONNÉES COLLECTÉES ===
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
    image_vue: str = None  # Null pour lien simple

# === ROUTE DE COLLECTE DES DONNÉES (FormSubmit ou JS tracker) ===
@app.post("/collecte")
async def collecter_infos(data: CollecteData):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO collectes_web (
                id_lien, ip, ville, region, pays, latitude, longitude,
                fai, os, navigateur, resolution, fuseau, date_collecte, image_vue
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            1,  # Tu peux remplacer 1 par l’ID réel si besoin
            data.ip, data.ville, data.region, data.pays,
            data.latitude, data.longitude, data.fai,
            data.os, data.navigateur, data.resolution,
            data.fuseau, data.date, data.image_vue
        ))

        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": "Collecte enregistrée dans la base"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
