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

# Define the names of the indexes to delete
indexes_to_delete = ["users", "workouts"]

# Delete the specified indexes
for index_name in indexes_to_delete:
    if client.indices.exists(index=index_name):
        client.indices.delete(index=index_name)
        print(f"Index '{index_name}' deleted successfully.")
    else:
        print(f"Index '{index_name}' does not exist.")

# Close the Elasticsearch client when done
client.close()
