import requests
import json

user_data = {
    "ID": "user3",
    "Username": "alice_wonder",
    "Password": "hashed_password_3"
}

response = requests.post("http://localhost:5000/api/users", json=user_data)
print(response.status_code)
print(response.json())
