import requests

user_id = "user1"

response = requests.get(f"http://localhost:5000/api/users/{user_id}/workouts")
print(response.status_code)
print(response.json())
