"""Test to verify the response format of the clients list endpoint"""
import requests
import json

print("Testing /nutricionistas/{id}/clientes endpoint response format\n")

# Login
login_response = requests.post(
    "http://localhost:8000/auth/login",
    json={"email": "teste@nutricionista.com", "senha": "senha123456"}
)

token = login_response.json().get("token")
user_id = login_response.json().get("id")
headers = {"Authorization": f"Bearer {token}"}

# Test the list endpoint
clients_response = requests.get(
    f"http://localhost:8000/nutricionistas/{user_id}/clientes?skip=0&limit=10",
    headers=headers
)

print(f"Status: {clients_response.status_code}")
print(f"Response type: {type(clients_response.json())}")
print(f"Response (first 3 items):")
print(json.dumps(clients_response.json()[:3], indent=2, default=str))

print(f"\n\nThe issue:")
print(f"- Backend returns: List[ClienteResponse]")
print(f"- Frontend expects: {{items: List, total_pages: int}}")
print(f"- Frontend code tries to access response.items which is undefined!")
