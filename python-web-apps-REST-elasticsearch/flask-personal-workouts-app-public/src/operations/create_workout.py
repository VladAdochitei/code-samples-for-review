import requests
import json

user_id = "user1"
workout_data = {
    "ID": "workout4",
    "UserId": user_id,
    "Type": "running",
    "Date": "2023-01-04",
    "Duration": 45
}

response = requests.post(f"http://localhost:5000/api/users/{user_id}/workouts", json=workout_data)
print(response.status_code)
print(response.json())
