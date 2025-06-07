import requests

def upload_to_gofile(file_path):
    try:
        # 1. Obtenir le serveur dynamique
        server_resp = requests.get("https://api.gofile.io/getServer")
        server_resp.raise_for_status()
        server = server_resp.json()["data"]["server"]

        # 2. Envoyer le fichier au bon serveur
        upload_url = f"https://{server}.gofile.io/uploadFile"

        with open(file_path, "rb") as f:
            files = {"file": f}
            upload_resp = requests.post(upload_url, files=files)

        upload_resp.raise_for_status()
        upload_data = upload_resp.json()

        if upload_data["status"] == "ok":
            return upload_data["data"]["downloadPage"]
        else:
            raise Exception(f"Erreur upload : {upload_data.get('message', 'Erreur inconnue')}")

    except requests.exceptions.RequestException as req_err:
        raise Exception(f"Erreur réseau GoFile : {str(req_err)}")
    except Exception as e:
        raise Exception(f"Erreur GoFile : {str(e)}")