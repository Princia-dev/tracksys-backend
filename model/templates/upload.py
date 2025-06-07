import requests

def upload_file_to_gofile(file_path):
    try:
        server_res = requests.get("https://api.gofile.io/getServer")
        server = server_res.json()['data']['server']

        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(f"https://{server}.gofile.io/uploadFile", files=files)
            result = response.json()

        if result['status'] == 'ok':
            return result['data']['downloadPage']
        else:
            print("Erreur upload :", result)
            return None
    except Exception as e:
        print("Erreur pendant upload :", e)
        return None