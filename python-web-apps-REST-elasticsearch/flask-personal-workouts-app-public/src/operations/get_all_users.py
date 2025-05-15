import requests

response = requests.get("http://localhost:5000/api/users")
print(response.status_code)
print(response.json())
