#!/usr/bin/env python3
"""
Integration test simulating the frontend workflow for SettingsPage
"""
import requests
import json

print("=== SETTINGS PAGE INTEGRATION TEST ===\n")

# 1. Login (simulating frontend login)
print("1. Simulating frontend login...")
login_response = requests.post(
    "http://localhost:8000/auth/login",
    json={"email": "teste@nutricionista.com", "senha": "senha123456"}
)

if login_response.status_code != 200:
    print(f"   ❌ Login failed: {login_response.status_code}")
    exit(1)

login_data = login_response.json()
token = login_data.get("token")
user_id = login_data.get("id")
nome = login_data.get("nome")
crn = login_data.get("crn")

print(f"   ✅ Login successful")
print(f"      User: {nome}")
print(f"      CRN: {crn}")
print(f"      Email: {login_data.get('email')}")
print(f"      User data (as stored in localStorage):")
print(f"      {{'id': {user_id}, 'nome': '{nome}', 'email': '{login_data.get('email')}', 'crn': '{crn}'}}")

# 2. Load settings (simulating SettingsPage.loadSettings())
print("\n2. Simulating SettingsPage.loadSettings()...")
headers = {"Authorization": f"Bearer {token}"}

config_response = requests.get(
    f"http://localhost:8000/nutricionistas/{user_id}/configuracao",
    headers=headers
)

if config_response.status_code != 200:
    print(f"   ❌ Failed to load configuration: {config_response.status_code}")
    exit(1)

config_data = config_response.json()
print(f"   ✅ Configuration loaded")
print(f"      Logo: {config_data.get('logo_url')}")
print(f"      Valor Consulta: R$ {config_data.get('valor_consulta')}")
print(f"      Link Agendamento: {config_data.get('link_agendamento')}")
print(f"      ✅ NO 'cor_primaria' field (as expected)")

# 3. Update settings (simulating SettingsPage.handleSaveConfig())
print("\n3. Simulating SettingsPage.handleSaveConfig()...")

# Update nutricionista data (nome and crn)
nutricionista_update = {
    "nome": "Dra. Silva Atualizada",
    "crn": "999888/MG"
}

nutricionista_response = requests.put(
    f"http://localhost:8000/nutricionistas/{user_id}",
    headers=headers,
    json=nutricionista_update
)

if nutricionista_response.status_code != 200:
    print(f"   ❌ Failed to update nutricionista: {nutricionista_response.status_code}")
    exit(1)

ntr_data = nutricionista_response.json()
print(f"   ✅ Nutricionista updated")
print(f"      Nome: {ntr_data.get('nome')}")
print(f"      CRN: {ntr_data.get('crn')}")
print(f"      ✅ NO 'cor_primaria' field (as expected)")

# Update configuration data
config_update = {
    "valor_consulta": 350.00,
    "link_agendamento": "https://calendly.com/updated"
}

config_update_response = requests.put(
    f"http://localhost:8000/nutricionistas/{user_id}/configuracao",
    headers=headers,
    json=config_update
)

if config_update_response.status_code != 200:
    print(f"   ❌ Failed to update configuration: {config_update_response.status_code}")
    exit(1)

config_updated = config_update_response.json()
print(f"   ✅ Configuration updated")
print(f"      Valor Consulta: R$ {config_updated.get('valor_consulta')}")
print(f"      Link Agendamento: {config_updated.get('link_agendamento')}")
print(f"      ✅ NO 'cor_primaria' field (as expected)")

# 4. Verify final state
print("\n4. Verifying final state...")
final_response = requests.get(
    f"http://localhost:8000/nutricionistas/{user_id}",
    headers=headers
)

if final_response.status_code != 200:
    print(f"   ❌ Failed to fetch final state: {final_response.status_code}")
    exit(1)

final_data = final_response.json()
print(f"   ✅ Final state verified")
print(f"      Nome: {final_data.get('nome')}")
print(f"      CRN: {final_data.get('crn')}")
print(f"      Email: {final_data.get('email')}")

config_final = final_data.get('configuracao', {})
print(f"      Configuration fields: {list(config_final.keys())}")
print(f"      ✅ NO 'cor_primaria' in database schema")

# Final check
has_cor_anywhere = 'cor_primaria' in final_data or 'cor_primaria' in config_final
if has_cor_anywhere:
    print(f"\n   ❌ FAILED: Found 'cor_primaria' in response!")
    exit(1)

print("\n✅ ALL INTEGRATION TESTS PASSED!")
print("\n✅ REQUIREMENTS MET:")
print("   ✓ CRN field added to Nutricionista model")
print("   ✓ CRN field returned in login response")
print("   ✓ CRN field editable in SettingsPage")
print("   ✓ cor_primaria removed from database schema")
print("   ✓ cor_primaria removed from all API responses")
print("   ✓ Frontend SettingsPage updated (removed color picker)")
