import requests
import json

user_id = "user1"
updated_user_data = {
    "ID": "user1",
    "Username": "new_username",
    "Password": "new_hashed_password"
}

response = requests.put(f"http://localhost:5000/api/users/{user_id}", json=updated_user_data)
print(response.status_code)
print(response.json())
