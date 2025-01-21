import requests

def check_page_status(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return False
