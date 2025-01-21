import requests

def check_page_status(url):
    """
    Verifica se a página foi carregada corretamente, retornando True se o código de status for 200.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lança uma exceção para códigos de status 4xx/5xx
        return True
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return False
