import pytest
from site_utils import check_page_status

# URLs a serem testadas
URLS_TO_TEST = [
    "https://aborgesdoamaral.streamlit.app",  # URL válida
            # URL inválida para teste
]

@pytest.mark.parametrize("url", URLS_TO_TEST)
def test_page_status(url):
    """
    Testa se a página foi carregada corretamente.
    """
    result = check_page_status(url)
    assert result is True, f"Falha ao carregar a página: {url}"
