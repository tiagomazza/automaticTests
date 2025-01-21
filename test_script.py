import pytest
import requests
import datetime

def check_page_status(url):
    """Função que verifica se a página foi carregada corretamente, retornando True se a resposta for 200 (OK)."""
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Teste para verificar se a página foi carregada corretamente
@pytest.mark.parametrize("url", ["https://aborgesdoamaral.streamlit.app"])
def test_page_status(url):
    """Teste para verificar se a página abriu corretamente."""
    result = check_page_status(url)
    assert result is True, f"Página não foi aberta corretamente. URL: {url}"

# Fixture para gerar o relatório de teste
@pytest.fixture(scope="session", autouse=True)
def generate_report(request):
    yield
    report_content = f"""
    <html>
    <head><title>Relatório de Teste - Verificação de Status da Página</title></head>
    <body>
    <h1>Relatório de Teste - Verificação de Status da Página</h1>
    <p>Data e hora da execução: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    <h2>Resultados:</h2>
    <ul>
    """
    
    for item in request.node.items:
        result = "Passou" if item.rep_call.passed else "Falhou"  # Acessar corretamente o resultado do item
        report_content += f"<li>{item.name}: {result}</li>"
    
    report_content += """
    </ul>
    </body>
    </html>
    """
    
    with open("test_report.html", "w") as f:
        f.write(report_content)

# Hook para gerar o relatório de execução de testes
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
