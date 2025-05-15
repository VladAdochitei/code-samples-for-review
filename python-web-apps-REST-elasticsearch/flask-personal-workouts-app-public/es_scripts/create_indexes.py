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

# Define the index settings and mappings for users
user_index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "ID": {"type": "keyword"},
            "Username": {"type": "keyword"},
            "Password": {"type": "keyword"},
        }
    }
}

# Define the index settings and mappings for workouts
workout_index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 1
    },
    "mappings": {
        "properties": {
            "ID": {"type": "keyword"},
            "UserId": {"type": "keyword"},
            "Type": {"type": "keyword"},
            "Date": {"type": "date"},
            "Duration": {"type": "integer"},
            "Distance": {"type": "float"},
            "Location": {"type": "geo_point"},
            "Notes": {"type": "text"}
        }
    }
}

# Create the "users" and "workouts" indices
user_index_name = "users"
workout_index_name = "workouts"

if not client.indices.exists(index=user_index_name):
    client.indices.create(index=user_index_name, body=user_index_settings)
    print(f"Index '{user_index_name}' created successfully.")
else:
    print(f"Index '{user_index_name}' already exists.")

if not client.indices.exists(index=workout_index_name):
    client.indices.create(index=workout_index_name, body=workout_index_settings)
    print(f"Index '{workout_index_name}' created successfully.")
else:
    print(f"Index '{workout_index_name}' already exists.")

# Close the Elasticsearch client when done
client.close()
