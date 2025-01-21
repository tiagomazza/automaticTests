import pytest  # Certifique-se de que o pytest está importado
import requests
import datetime

# Função de verificação de status
def test_check_page_status(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

@pytest.fixture(scope="session", autouse=True)
def generate_report(request):
    """Gera um relatório em HTML com os resultados dos testes."""
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
        # Certifique-se de que `rep_call` existe antes de acessá-lo
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
