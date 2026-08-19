import os

import chromadb
from dotenv import load_dotenv

load_dotenv(override=True)

COLLECTION_NAME = os.getenv("CHROMA_COLLECTION", "solar_knowledge")


def get_collection():
    client = chromadb.CloudClient(
        api_key=os.getenv("CHROMA_API_KEY"),
        tenant=os.getenv("CHROMA_TENANT"),
        database=os.getenv("CHROMA_DATABASE"),
    )
    return client.get_or_create_collection(COLLECTION_NAME)
