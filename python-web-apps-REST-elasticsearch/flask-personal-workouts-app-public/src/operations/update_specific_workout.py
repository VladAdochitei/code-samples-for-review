import requests
import json

user_id = "user1"
workout_id = "workout1"
updated_workout_data = {
    "ID": workout_id,
    "UserId": user_id,
    "Type": "swimming",
    "Date": "2023-01-05",
    "Duration": 60
}

response = requests.put(f"http://localhost:5000/api/users/{user_id}/workouts/{workout_id}", json=updated_workout_data)
print(response.status_code)
print(response.json())
