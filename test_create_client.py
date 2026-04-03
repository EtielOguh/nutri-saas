#!/usr/bin/env python3
"""Script para testar criação de cliente."""
import requests
import json

BASE_URL = "http://localhost:8000"

# Credenciais de teste
EMAIL = "teste@nutricionista.com"
SENHA = "senha123456"

print("🔍 Testando criação de cliente\n")

# 1. Login
print("1️⃣ Fazendo login...")
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": EMAIL,
    "senha": SENHA
})
if response.status_code != 200:
    print(f"❌ Erro login: {response.text}")
    exit(1)

data = response.json()
token = data.get('token')
nutricionista_id = data.get('id')
print(f"✅ Token obtido!")

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 2. Tentar criar cliente
print("\n2️⃣ Tentando criar cliente...")

client_data = {
    "nutricionista_id": nutricionista_id,
    "name": "Maria Silva",
    "email": "maria@email.com",
    "phone": "(11) 99999-9999",
    "age": 35,
    "height": 1.70,
    "gender": "feminino",
    "initial_weight": 75.5,
    "objective": "Perder peso",
    "notes": "Sem restrições alimentares"
}

print(f"Enviando dados: {json.dumps(client_data, indent=2)}")

response = requests.post(
    f"{BASE_URL}/nutricionistas/{nutricionista_id}/clientes",
    headers=headers,
    json=client_data
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

if response.status_code == 201:
    print("✅ Cliente criado com sucesso!")
else:
    print(f"❌ Erro ao criar cliente")
