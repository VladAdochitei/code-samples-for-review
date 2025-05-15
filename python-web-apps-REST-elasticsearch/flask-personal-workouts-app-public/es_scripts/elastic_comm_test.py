from elasticsearch import Elasticsearch
import os

api_key_id = os.getenv("API_KEY_ID")
api_key_secret = os.getenv("API_KEY_SECRET")


client = Elasticsearch(
    "https://1f541cf6aa7e45d8a0e3cf74dd75f439.us-central1.gcp.cloud.es.io",  # Elasticsearch endpoint
    api_key=(api_key_id, api_key_secret),  # API key ID and secret
)

client.indices.create(index="my_index")

client.index(
    index="my_index",
    id="my_document_id",
    document={
        "foo": "foo",
        "bar": "bar",
    }
)

