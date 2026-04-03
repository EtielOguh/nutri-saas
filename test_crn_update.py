import requests
import json

# Login test
login_response = requests.post(
    "http://localhost:8000/auth/login",
    json={"email": "teste@nutricionista.com", "senha": "senha123456"}
)

print("Login Response:", login_response.status_code)
data = login_response.json()
print(json.dumps(data, indent=2))

if login_response.status_code == 200:
    token = data.get("token")  # Changed from "access_token" to "token"
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test updating nutricionista with nome and crn
    print("\n--- Testing PUT /nutricionistas/1 with nome and crn ---")
    update_response = requests.put(
        "http://localhost:8000/nutricionistas/1",
        headers=headers,
        json={
            "nome": "Dr. João Silva",
            "crn": "123456/SP"
        }
    )
    
    print("Update Response:", update_response.status_code)
    print(json.dumps(update_response.json(), indent=2))
    
    # Get nutricionista to verify
    print("\n--- Getting nutricionista to verify ---")
    get_response = requests.get(
        "http://localhost:8000/nutricionistas/1",
        headers=headers
    )
    print("Get Response:", get_response.status_code)
    print(json.dumps(get_response.json(), indent=2))
