"""Test script to diagnose client data loading and image serving issues"""
import requests
import json

print("=== DIAGNOSTICS TEST ===\n")

# 1. Login
print("1. Testing login...")
login_response = requests.post(
    "http://localhost:8000/auth/login",
    json={"email": "teste@nutricionista.com", "senha": "senha123456"}
)

if login_response.status_code != 200:
    print(f"   ❌ Login failed: {login_response.status_code}")
    print(f"      {login_response.text}")
    exit(1)

login_data = login_response.json()
token = login_data.get("token")
user_id = login_data.get("id")
headers = {"Authorization": f"Bearer {token}"}
print(f"   ✅ Login successful (ID: {user_id})")

# 2. Get list of clients
print("\n2. Testing GET /nutricionistas/{id}/clientes...")
clients_response = requests.get(
    f"http://localhost:8000/nutricionistas/{user_id}/clientes",
    headers=headers
)

if clients_response.status_code != 200:
    print(f"   ❌ Failed: {clients_response.status_code}")
    print(f"      {clients_response.text}")
    exit(1)

clients = clients_response.json()
print(f"   ✅ Got {len(clients)} clients")

if len(clients) > 0:
    client_id = clients[0]['id']
    print(f"\n3. Testing GET /clientes/{client_id}...")
    
    # Try the direct endpoint that frontend uses
    client_response = requests.get(
        f"http://localhost:8000/clientes/{client_id}",
        headers=headers
    )
    
    if client_response.status_code != 200:
        print(f"   ❌ Failed: {client_response.status_code}")
        print(f"      Response: {client_response.text}")
    else:
        client_data = client_response.json()
        print(f"   ✅ Got client data")
        print(f"      Client: {client_data.get('nome')}")
        print(f"      ID: {client_data.get('id')}")
        print(f"      Email: {client_data.get('email')}")
        print(f"      Fields: {list(client_data.keys())}")

# 4. Test image serving
print("\n4. Testing image serving...")
# Get a logo filename from the config
config_response = requests.get(
    f"http://localhost:8000/nutricionistas/{user_id}/configuracao",
    headers=headers
)

if config_response.status_code == 200:
    config = config_response.json()
    logo_url = config.get('logo_url')
    
    if logo_url:
        print(f"   Logo URL from API: {logo_url}")
        
        # Test if the logo is served correctly
        if logo_url.startswith('/'):
            # Relative URL - try serving it
            logo_response = requests.get(f"http://localhost:8000{logo_url}")
            if logo_response.status_code == 200:
                print(f"   ✅ Logo served successfully (size: {len(logo_response.content)} bytes)")
            else:
                print(f"   ❌ Logo serving failed: {logo_response.status_code}")
                print(f"      URL tried: http://localhost:8000{logo_url}")
        else:
            print(f"   Logo URL is not relative - check frontend handling")
    else:
        print(f"   No logo URL in config")
else:
    print(f"   ❌ Failed to get config: {config_response.status_code}")

print("\n=== DIAGNOSTICS COMPLETE ===")
