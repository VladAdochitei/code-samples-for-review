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

# Define sample user data
user_data = [
    {"ID": "user1", "Username": "john_doe", "Password": "hashed_password_1"},
    {"ID": "user2", "Username": "jane_smith", "Password": "hashed_password_2"},
    # Add more user data as needed
]

# Index the sample user data into the "users" index
index_name = "users"
for user in user_data:
    client.index(index=index_name, body=user)

# Close the Elasticsearch client when done
client.close()
