import pytest
from script import check_phrase_in_site
import datetime

@pytest.fixture(scope="session")
def execution_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def test_phrase_found(execution_time):
    """Teste quando a frase está presente no site."""
    url = "https://aborgesdoamaral.streamlit.app"
    phrase = "Ponto"
    result = check_phrase_in_site(url, phrase)
    assert result is True, f"Frase encontrada no site. Tempo de execução: {execution_time}"


@pytest.fixture(scope="session", autouse=True)
def generate_report(request):
    yield
    report_content = f"""
    <html>
    <head><title>Relatório de Teste - Verificação de Frase</title></head>
    <body>
    <h1>Relatório de Teste - Verificação de Frase</h1>
    <p>Data e hora da execução: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <h2>Resultados:</h2>
    <ul>
    """
    
    for item in request.node.items:
        result = "Passou" if item.rep_call.passed else "Falhou"
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
