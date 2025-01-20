import requests
from bs4 import BeautifulSoup

def check_phrase_in_site(url, phrase):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
   
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return phrase in soup.get_text()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o site: {e}")
        return False


