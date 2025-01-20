import requests
from bs4 import BeautifulSoup

def check_phrase_in_site(url, phrase):
   
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        return phrase in soup.get_text()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar o site: {e}")
        return False

if __name__ == "__main__":
    url = "https://aborgesdoamaral.pt"
    phrase = "tudo o que precisa para"
    if check_phrase_in_site(url, phrase):
        print("Frase encontrada!")
    else:
        print("Frase não encontrada.")
