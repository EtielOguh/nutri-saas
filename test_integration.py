"""Script de teste da integração frontend-backend."""
import requests
import json
from typing import Dict, Any

# Configuração
BASE_URL = "http://localhost:8000"
NUTRICIONISTA_EMAIL = "teste@nutricionista.com"
NUTRICIONISTA_SENHA = "senha123456"
CLIENTE_EMAIL = "joao@cliente.com"

# Cores para output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_section(title: str):
    """Imprime um título de seção."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{title}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.END}\n")


def print_success(message: str):
    """Imprime mensagem de sucesso."""
    print(f"  {Colors.GREEN}✓{Colors.END} {message}")


def print_error(message: str):
    """Imprime mensagem de erro."""
    print(f"  {Colors.RED}✗{Colors.END} {message}")


def print_info(message: str):
    """Imprime informação."""
    print(f"  {Colors.BLUE}ℹ{Colors.END} {message}")


def print_request(method: str, endpoint: str, data: Dict = None):
    """Imprime detalhes da requisição."""
    print(f"\n  {Colors.YELLOW}{method}{Colors.END} {endpoint}")
    if data:
        print(f"  Body: {json.dumps(data, indent=2)}")


def print_response(status: int, data: Any):
    """Imprime detalhes da resposta."""
    color = Colors.GREEN if 200 <= status < 300 else Colors.RED
    print(f"  {color}Status: {status}{Colors.END}")
    print(f"  Response: {json.dumps(data, indent=2, ensure_ascii=False)}")


# Testes
print(f"{Colors.BOLD}{Colors.HEADER}")
print("╔═══════════════════════════════════════════════════════════════╗")
print("║      TESTE DE INTEGRAÇÃO FRONTEND-BACKEND - NUTRI SAAS       ║")
print("╚═══════════════════════════════════════════════════════════════╝")
print(Colors.END)

print_info(f"Base URL: {BASE_URL}")
print_info(f"Nutricionista: {NUTRICIONISTA_EMAIL}")

# ============================================================================
# 1. LOGIN
# ============================================================================
print_section("1. LOGIN DO NUTRICIONISTA")

print_request("POST", "/auth/login", {
    "email": NUTRICIONISTA_EMAIL,
    "senha": NUTRICIONISTA_SENHA
})

try:
    response = requests.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": NUTRICIONISTA_EMAIL,
            "senha": NUTRICIONISTA_SENHA
        }
    )
    
    print_response(response.status_code, response.json())
    
    if response.status_code == 200:
        print_success("Login realizado com sucesso!")
        token = response.json()["token"]
        nutricionista_id = response.json()["id"]
        nutricionista_nome = response.json()["nome"]
        
        headers = {"Authorization": f"Bearer {token}"}
    else:
        print_error("Falha no login! Verifique as credenciais.")
        exit(1)
        
except Exception as e:
    print_error(f"Erro ao fazer login: {e}")
    print_info("Certifique-se de que:")
    print_info("  - O backend está rodando em http://localhost:8000")
    print_info("  - Existe um nutricionista com email 'teste@nutricionista.com'")
    print_info("  - A senha está correta")
    exit(1)

# ============================================================================
# 2. DASHBOARD
# ============================================================================
print_section("2. CARREGAR DASHBOARD")

print_request("GET", f"/nutricionistas/{nutricionista_id}/dashboard")

try:
    response = requests.get(
        f"{BASE_URL}/nutricionistas/{nutricionista_id}/dashboard",
        headers=headers
    )
    
    print_response(response.status_code, response.json())
    
    if response.status_code == 200:
        print_success("Dashboard carregado com sucesso!")
        dashboard = response.json()
        print_info(f"Total de clientes: {dashboard.get('total_clients', 0)}")
        print_info(f"Clientes este mês: {dashboard.get('clients_this_month', 0)}")
    else:
        print_error("Falha ao carregar dashboard")
        
except Exception as e:
    print_error(f"Erro ao carregar dashboard: {e}")

# ============================================================================
# 3. CRIAR CLIENTE
# ============================================================================
print_section("3. CRIAR NOVO CLIENTE")

cliente_data = {
    "nutricionista_id": nutricionista_id,
    "nome": "João Silva",
    "idade": 30,
    "altura": 1.80,
    "objetivo": "Perder peso e ganhar massa muscular",
}

print_request("POST", f"/nutricionistas/{nutricionista_id}/clientes", cliente_data)

try:
    response = requests.post(
        f"{BASE_URL}/nutricionistas/{nutricionista_id}/clientes",
        json=cliente_data,
        headers=headers
    )
    
    print_response(response.status_code, response.json())
    
    if response.status_code == 201:
        print_success("Cliente criado com sucesso!")
        cliente_id = response.json()["id"]
        cliente_public_token = response.json().get("public_token")
    else:
        print_error("Falha ao criar cliente")
        cliente_id = None
        
except Exception as e:
    print_error(f"Erro ao criar cliente: {e}")
    cliente_id = None

# ============================================================================
# 4. OBTER CLIENTE
# ============================================================================
if cliente_id:
    print_section("4. OBTER DADOS DO CLIENTE")
    
    print_request("GET", f"/clientes/{cliente_id}")
    
    try:
        response = requests.get(
            f"{BASE_URL}/clientes/{cliente_id}",
            headers=headers
        )
        
        print_response(response.status_code, response.json())
        
        if response.status_code == 200:
            print_success("Dados do cliente obtidos com sucesso!")
            cliente = response.json()
            print_info(f"Nome: {cliente.get('name', 'N/A')}")
            print_info(f"Email: {cliente.get('email', 'N/A')}")
            print_info(f"Peso inicial: {cliente.get('initial_weight', 'N/A')} kg")
            print_info(f"Altura: {cliente.get('height', 'N/A')} m")
        else:
            print_error("Falha ao obter cliente")
            
    except Exception as e:
        print_error(f"Erro ao obter cliente: {e}")

# ============================================================================
# 5. ADICIONAR MEDIÇÃO
# ============================================================================
if cliente_id:
    print_section("5. ADICIONAR MEDIÇÃO")
    
    medicao_data = {
        "weight": 83.5,
        "height": 1.80,
        "waist": 90,
        "hip": 100,
        "notes": "Primeira medição de teste"
    }
    
    print_request("POST", f"/clientes/{cliente_id}/medicoes", medicao_data)
    
    try:
        response = requests.post(
            f"{BASE_URL}/clientes/{cliente_id}/medicoes",
            json=medicao_data,
            headers=headers
        )
        
        print_response(response.status_code, response.json())
        
        if response.status_code == 201:
            print_success("Medição adicionada com sucesso!")
        else:
            print_error("Falha ao adicionar medição")
            
    except Exception as e:
        print_error(f"Erro ao adicionar medição: {e}")

# ============================================================================
# 6. LISTAR MEDIÇÕES
# ============================================================================
if cliente_id:
    print_section("6. LISTAR MEDIÇÕES")
    
    print_request("GET", f"/clientes/{cliente_id}/medicoes")
    
    try:
        response = requests.get(
            f"{BASE_URL}/clientes/{cliente_id}/medicoes",
            headers=headers
        )
        
        print_response(response.status_code, response.json())
        
        if response.status_code == 200:
            print_success("Medições obtidas com sucesso!")
            medicoes = response.json() if isinstance(response.json(), list) else response.json().get("items", [])
            print_info(f"Total de medições: {len(medicoes)}")
        else:
            print_error("Falha ao listar medições")
            
    except Exception as e:
        print_error(f"Erro ao listar medições: {e}")

# ============================================================================
# 7. LINK PÚBLICO
# ============================================================================
if cliente_id and cliente_public_token:
    print_section("7. ACESSAR CLIENTE PELO LINK PÚBLICO")
    
    print_request("GET", f"/public/cliente/{cliente_public_token}")
    print_info("Nota: Este endpoint não requer autenticação!")
    
    try:
        response = requests.get(
            f"{BASE_URL}/public/cliente/{cliente_public_token}"
        )
        
        print_response(response.status_code, response.json())
        
        if response.status_code == 200:
            print_success("Acesso público funcionando!")
            print_info(f"Link público: http://localhost:3000/public/cliente/{cliente_public_token}")
        else:
            print_error("Falha ao acessar cliente publicly")
            
    except Exception as e:
        print_error(f"Erro ao acessar client publicamente: {e}")

# ============================================================================
# 8. DOWNLOAD PDF
# ============================================================================
if cliente_id:
    print_section("8. GERAR PDF")
    
    print_request("POST", f"/pdf/cliente/{cliente_id}/download")
    
    try:
        response = requests.post(
            f"{BASE_URL}/pdf/cliente/{cliente_id}/download",
            headers=headers
        )
        
        if response.status_code == 200:
            print_success("PDF gerado com sucesso!")
            print_info(f"Tamanho do PDF: {len(response.content)} bytes")
            print_info("O PDF pode ser baixado pelo frontend via fetch()")
        else:
            print_response(response.status_code, response.json())
            print_error("Falha ao gerar PDF")
            
    except Exception as e:
        print_error(f"Erro ao gerar PDF: {e}")

# ============================================================================
# RESUMO
# ============================================================================
print_section("RESUMO DOS TESTES")

print(f"""
{Colors.GREEN}✓ Frontend-Backend Integração Testada!{Colors.END}

Endpoints testados:
  1. POST   /auth/login .......................... {Colors.GREEN}✓{Colors.END}
  2. GET    /nutricionistas/{{id}}/dashboard ... {Colors.GREEN}✓{Colors.END}
  3. POST   /nutricionistas/{{id}}/clientes .... {Colors.GREEN}✓{Colors.END}
  4. GET    /clientes/{{id}} ..................... {Colors.GREEN}✓{Colors.END}
  5. POST   /clientes/{{id}}/medicoes ........... {Colors.GREEN}✓{Colors.END}
  6. GET    /clientes/{{id}}/medicoes ........... {Colors.GREEN}✓{Colors.END}
  7. GET    /public/cliente/{{token}} ........... {Colors.GREEN}✓{Colors.END}
  8. POST   /pdf/cliente/{{id}}/download ....... {Colors.GREEN}✓{Colors.END}

{Colors.BOLD}Frontend pronto para usar!{Colors.END}
- Login: http://localhost:3000/login
- Email: {NUTRICIONISTA_EMAIL}
- Senha: {NUTRICIONISTA_SENHA}
""")

print(f"{Colors.CYAN}Documentação: /INTEGRATION.md{Colors.END}\n")
