from elasticsearch import Elasticsearch
import os

# Define the Elasticsearch endpoint and API key
es_endpoint = "https://1f541cf6aa7e45d8a0e3cf74dd75f439.us-central1.gcp.cloud.es.io"
api_key_id = os.getenv("API_KEY_ID")
api_key_secret = os.getenv("API_KEY_SECRET")


# Initialize the Elasticsearch client with API key authentication
client = Elasticsearch(
    hosts=[es_endpoint],
    api_key=(api_key_id, api_key_secret)
)

# Define sample workout data
workout_data = [
    {"ID": "workout1", "UserId": "user1", "Type": "running", "Date": "2023-01-01", "Duration": 60},
    {"ID": "workout2", "UserId": "user2", "Type": "swimming", "Date": "2023-01-02", "Duration": 45},
    # Add more workout data as needed
]

# Index the sample workout data into the "workouts" index
index_name = "workouts"
for workout in workout_data:
    client.index(index=index_name, body=workout)

# Close the Elasticsearch client when done
client.close()
