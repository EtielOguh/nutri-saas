#!/usr/bin/env python3
"""Script para testar endpoints da API."""
import requests
import json
from pathlib import Path

BASE_URL = "http://localhost:8000"

# Credenciais de teste
EMAIL = "teste@nutricionista.com"
SENHA = "senha123456"

print("🔍 Testando endpoints da API\n")

# 1. Login
print("1️⃣ Testando login...")
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": EMAIL,
    "senha": SENHA
})
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    token = data.get('token')
    nutricionista_id = data.get('id')
    print(f"✅ Autenticado! Token: {token[:20]}...")
    print(f"   Nutricionista ID: {nutricionista_id}")
else:
    print(f"❌ Erro: {response.text}")
    exit(1)

# Headers com autenticação
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 2. Obter configurações
print(f"\n2️⃣ Testando GET /nutricionistas/{nutricionista_id}/configuracao...")
response = requests.get(
    f"{BASE_URL}/nutricionistas/{nutricionista_id}/configuracao",
    headers=headers
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    config = response.json()
    print(f"✅ Configurações obtidas!")
    print(f"   {json.dumps(config, indent=2)}")
elif response.status_code == 404:
    print(f"⚠️ Configurações não encontradas (irá criar padrão)")
else:
    print(f"❌ Erro: {response.text}")

# 3. Listar clientes
print(f"\n3️⃣ Testando GET /nutricionistas/{nutricionista_id}/clientes...")
response = requests.get(
    f"{BASE_URL}/nutricionistas/{nutricionista_id}/clientes",
    headers=headers,
    params={"skip": 0, "limit": 10}
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    clientes = response.json()
    print(f"✅ Clientes obtidos!")
    print(f"   Total: {len(clientes)} clientes")
    if clientes:
        print(f"   Primeiro cliente: {clientes[0].get('nome', 'N/A')}")
else:
    print(f"❌ Erro: {response.text}")

# 4. Upload de logo (teste com arquivo de teste)
print(f"\n4️⃣ Testando POST /nutricionistas/{nutricionista_id}/upload-logo...")
test_image = Path("frontend/public/vite.svg")
if test_image.exists():
    with open(test_image, "rb") as f:
        files = {"file": ("test.svg", f, "image/svg+xml")}
        response = requests.post(
            f"{BASE_URL}/nutricionistas/{nutricionista_id}/upload-logo",
            headers={"Authorization": f"Bearer {token}"},
            files=files
        )
    print(f"Status: {response.status_code}")
    if response.status_code == 201:
        result = response.json()
        print(f"✅ Logo enviada!")
        print(f"   URL: {result.get('logo_url')}")
    else:
        print(f"❌ Erro: {response.text}")
else:
    print(f"⚠️ Arquivo de teste não encontrado")

# 5. Atualizar configurações
print(f"\n5️⃣ Testando PUT /nutricionistas/{nutricionista_id}/configuracao...")
response = requests.put(
    f"{BASE_URL}/nutricionistas/{nutricionista_id}/configuracao",
    headers=headers,
    json={
        "cor_primaria": "#2e7d32",
        "valor_consulta": 150.00,
        "link_agendamento": "https://example.com/agendamento"
    }
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    config = response.json()
    print(f"✅ Configurações atualizadas!")
    print(f"   {json.dumps(config, indent=2)}")
else:
    print(f"❌ Erro: {response.text}")

print("\n✨ Testes concluídos!")
