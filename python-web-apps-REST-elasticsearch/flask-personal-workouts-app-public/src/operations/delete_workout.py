import requests

user_id = "user1"
workout_id = "workout1"

response = requests.delete(f"http://localhost:5000/api/users/{user_id}/workouts/{workout_id}")
print(response.status_code)
print(response.json())
