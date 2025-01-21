import pytest
from site_utils import check_page_status
import datetime

# URLs a serem testadas
URLS_TO_TEST = [
    "https://aborgesdoamaral.streamlit.app",  # URL válida
    "https://aborgesdoamaral.pt"
]

@pytest.mark.parametrize("url", URLS_TO_TEST)
def test_page_status(url):
    """
    Testa se a página foi carregada corretamente.
    """
    result = check_page_status(url)
    assert result is True, f"Falha ao carregar a página: {url}"


# Fixture para gerar o relatório
@pytest.fixture(scope="session", autouse=True)
def generate_report(request):
    """
    Gera um relatório em HTML com os resultados dos testes após a execução.
    """
    yield  # Aguarda a execução dos testes

    # Conteúdo inicial do relatório
    report_content = f"""
    <html>
    <head><title>Relatório de Testes</title></head>
    <body>
    <h1>Relatório de Testes</h1>
    <p>Data e hora de execução: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <h2>Resultados:</h2>
    <ul>
    """

    # Adiciona os resultados dos testes ao relatório
    for item in request.node.items:
        rep_call = getattr(item, "rep_call", None)
        if rep_call is not None:
            result = "Passou" if rep_call.passed else "Falhou"
        else:
            result = "Resultado desconhecido"
        report_content += f"<li>{item.name}: {result}</li>"

    # Finaliza o conteúdo do relatório
    report_content += """
    </ul>
    </body>
    </html>
    """

    # Salva o relatório em um arquivo HTML
    with open("test_report.html", "w") as f:
        f.write(report_content)


# Hook para capturar o resultado de cada teste
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook para capturar os resultados dos testes.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
