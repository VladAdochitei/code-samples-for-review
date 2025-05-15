import requests

user_id = "user1"

response = requests.delete(f"http://localhost:5000/api/users/{user_id}")
print(response.status_code)
print(response.json())
