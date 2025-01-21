import pytest
from site_utils import check_page_status
import datetime

URLS_TO_TEST = [
    "https://aborgesdoamaral.streamlit.app", 
   # "http://aborgesdoamaral.pt"
]

@pytest.mark.parametrize("url", URLS_TO_TEST)
def test_page_status(url):
    result = check_page_status(url)
    assert result is True, f"Falha ao carregar a página: {url}"

# Fixture para gerar o relatório
@pytest.fixture(scope="session", autouse=True)
def generate_report(request):
    yield 

    report_content = f"""
    <html>
    <head><title>Relatório de Testes</title></head>
    <body>
    <h1>Relatório de Testes</h1>
    <p>Data e hora de execução: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <h2>Resultados:</h2>
    <ul>
    """

    for item in request.node.items:
        rep_call = getattr(item, "rep_call", None)
        if rep_call is not None:
            result = "Passou" if rep_call.passed else "Falhou"
        else:
            result = "Resultado desconhecido"
        report_content += f"<li>{item.name}: {result}</li>"

    report_content += """
    </ul>
    </body>
    </html>
    """

 with open("test_report.html", "w") as f:
        f.write(report_content)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
