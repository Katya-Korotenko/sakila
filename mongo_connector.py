import os
from typing import Any
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.collection import Collection

load_dotenv('.env')

_client: MongoClient = MongoClient(os.getenv("MONGO_URI"))


def get_mongo_collection() -> Collection[dict[str, Any]]:
    """Retrieves the targeted MongoDB collection instance for search logging."""
    db_name: str = os.getenv("MONGO_DB", "test")
    collection_name: str = os.getenv("MONGO_COLLECTION", "search_history")
    return _client[db_name][collection_name]


def close_connection() -> None:
    """Safely terminates the active MongoDB client connection session."""
    _client.close()