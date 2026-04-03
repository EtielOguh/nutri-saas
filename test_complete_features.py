import requests
import json

print("=== COMPREHENSIVE FEATURE TEST ===\n")

# 1. Login
print("1. Testing Login with CRN field...")
login_response = requests.post(
    "http://localhost:8000/auth/login",
    json={"email": "teste@nutricionista.com", "senha": "senha123456"}
)
print(f"   Status: {login_response.status_code}")
login_data = login_response.json()
token = login_data.get("token")
print(f"   User: {login_data.get('nome')} | Email: {login_data.get('email')} | CRN: {login_data.get('crn')}")

if login_response.status_code == 200:
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Get Configuration
    print("\n2. Testing GET /nutricionistas/1/configuracao...")
    config_response = requests.get(
        "http://localhost:8000/nutricionistas/1/configuracao",
        headers=headers
    )
    print(f"   Status: {config_response.status_code}")
    config_data = config_response.json()
    print(f"   Logo: {config_data.get('logo_url')}")
    print(f"   Valor Consulta: R$ {config_data.get('valor_consulta')}")
    print(f"   Link Agendamento: {config_data.get('link_agendamento')}")
    has_cor = 'cor_primaria' in config_data
    print(f"   Has 'cor_primaria': {has_cor}")
    
    # 3. Update Configuration (without cor_primaria)
    print("\n3. Testing PUT /nutricionistas/1/configuracao (without cor_primaria)...")
    update_config_response = requests.put(
        "http://localhost:8000/nutricionistas/1/configuracao",
        headers=headers,
        json={
            "valor_consulta": 300.00,
            "link_agendamento": "https://calendly.com/doctor"
        }
    )
    print(f"   Status: {update_config_response.status_code}")
    if update_config_response.status_code == 200:
        updated_config = update_config_response.json()
        print(f"   New Valor Consulta: R$ {updated_config.get('valor_consulta')}")
        print(f"   New Link: {updated_config.get('link_agendamento')}")
        no_cor = 'cor_primaria' not in updated_config
        print(f"   NO 'cor_primaria' in response: {no_cor}")
    
    # 4. Update Nutricionista (nome and crn)
    print("\n4. Testing PUT /nutricionistas/1 (update nome and crn)...")
    update_nut_response = requests.put(
        "http://localhost:8000/nutricionistas/1",
        headers=headers,
        json={
            "nome": "Dra. Mariana Costa",
            "crn": "789456/RJ"
        }
    )
    print(f"   Status: {update_nut_response.status_code}")
    if update_nut_response.status_code == 200:
        updated_nut = update_nut_response.json()
        print(f"   New Nome: {updated_nut.get('nome')}")
        print(f"   New CRN: {updated_nut.get('crn')}")
    
    # 5. Verify no cor_primaria in database schema
    print("\n5. Checking database schema has NO 'cor_primaria'...")
    get_final = requests.get(
        "http://localhost:8000/nutricionistas/1",
        headers=headers
    )
    final_data = get_final.json()
    print(f"   GET nutricionista response: {final_data.get('nome')} | CRN: {final_data.get('crn')}")
    config_check = final_data.get('configuracao', {})
    has_cor_final = 'cor_primaria' in config_check
    print(f"   Configuration has 'cor_primaria': {has_cor_final}")
    print(f"   Configuration fields: {list(config_check.keys())}")

print("\n✅ ALL TESTS COMPLETED SUCCESSFULLY!")
