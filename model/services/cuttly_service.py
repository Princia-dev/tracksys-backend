import requests

def shorten_url_cuttly(long_url: str, api_key: str) -> str:
    endpoint = "https://cutt.ly/api/api.php"
    params = {
        "key": api_key,
        "short": long_url
    }

    try:
        response = requests.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("url", {}).get("status") == 7:
            return data["url"]["shortLink"]
        else:
            error_msg = data.get("url", {}).get("title", "Lien non raccourci")
            raise Exception(f"Erreur Cutt.ly : {error_msg}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erreur de connexion à Cutt.ly : {e}")
    except Exception as e:
        raise Exception(f"Erreur lors du raccourcissement : {e}")