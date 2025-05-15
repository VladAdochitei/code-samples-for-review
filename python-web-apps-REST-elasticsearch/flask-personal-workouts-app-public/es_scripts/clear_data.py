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

# Define the names of the indexes to delete all entries from
indexes_to_clear = ["users", "workouts"]

# Delete all entries in the specified indexes
for index_name in indexes_to_clear:
    if client.indices.exists(index=index_name):
        # Use the delete by query API to delete all documents in the index
        client.delete_by_query(index=index_name, body={"query": {"match_all": {}}})
        print(f"All entries in index '{index_name}' deleted successfully.")
    else:
        print(f"Index '{index_name}' does not exist.")

# Close the Elasticsearch client when done
client.close()
