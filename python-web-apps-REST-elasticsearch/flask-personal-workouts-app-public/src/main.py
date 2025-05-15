import os
from flask import Flask, jsonify, request, abort
from elasticsearch import Elasticsearch

app = Flask(__name__)

# Define the Elasticsearch endpoint and API key
es_endpoint = "https://1f541cf6aa7e45d8a0e3cf74dd75f439.us-central1.gcp.cloud.es.io"
api_key_id = os.getenv("API_KEY_ID")
api_key_secret = os.getenv("API_KEY_SECRET")


# Initialize the Elasticsearch client with API key authentication
client = Elasticsearch(
    hosts=[es_endpoint],
    api_key=(api_key_id, api_key_secret)
)

@app.route('/api/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        # Logic to get all users from Elasticsearch
        users_data = client.search(index="users", body={"query": {"match_all": {}}})
        users_list = [user["_source"] for user in users_data["hits"]["hits"]]
        return jsonify(users_list)
    elif request.method == 'POST':
        # Logic to create a new user in Elasticsearch
        new_user_data = request.get_json()
        response = client.index(index="users", body=new_user_data)
        return jsonify({"message": "User created successfully", "user_id": response["_id"]}), 201

@app.route('/api/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
        # Logic to get a specific user by ID from Elasticsearch
        user_data = client.get(index="users", id=user_id)
        if user_data["found"]:
            return jsonify(user_data["_source"])
        else:
            abort(404, description="User not found")

    elif request.method == 'PUT':
        # Logic to update user details in Elasticsearch
        updated_user_data = request.get_json()
        response = client.index(index="users", id=user_id, body=updated_user_data)
        return jsonify({"message": "User updated successfully", "user_id": response["_id"]})

    elif request.method == 'DELETE':
        # Logic to delete a user from Elasticsearch
        response = client.delete(index="users", id=user_id)
        if response["result"] == "deleted":
            return jsonify({"message": "User deleted successfully"})
        else:
            abort(404, description="User not found")

@app.route('/api/users/<user_id>/workouts', methods=['GET', 'POST'])
def workouts(user_id):
    if request.method == 'GET':
        # Logic to get all workouts for a specific user from Elasticsearch
        workouts_data = client.search(index="workouts", body={"query": {"term": {"UserId": user_id}}})
        workouts_list = [workout["_source"] for workout in workouts_data["hits"]["hits"]]
        return jsonify(workouts_list)

    elif request.method == 'POST':
        # Logic to create a new workout for a specific user in Elasticsearch
        new_workout_data = request.get_json()
        response = client.index(index="workouts", body=new_workout_data)
        return jsonify({"message": "Workout created successfully", "workout_id": response["_id"]}), 201

@app.route('/api/users/<user_id>/workouts/<workout_id>', methods=['GET', 'PUT', 'DELETE'])
def workout(user_id, workout_id):
    if request.method == 'GET':
        # Logic to get a specific workout for a user from Elasticsearch
        workout_data = client.get(index="workouts", id=workout_id)
        if workout_data["found"]:
            return jsonify(workout_data["_source"])
        else:
            abort(404, description="Workout not found")

    elif request.method == 'PUT':
        # Logic to update a specific workout for a user in Elasticsearch
        updated_workout_data = request.get_json()
        response = client.index(index="workouts", id=workout_id, body=updated_workout_data)
        return jsonify({"message": "Workout updated successfully", "workout_id": response["_id"]})

    elif request.method == 'DELETE':
        # Logic to delete a specific workout for a user in Elasticsearch
        response = client.delete(index="workouts", id=workout_id)
        if response["result"] == "deleted":
            return jsonify({"message": "Workout deleted successfully"})
        else:
            abort(404, description="Workout not found")

if __name__ == '__main__':
    app.run(debug=True)
