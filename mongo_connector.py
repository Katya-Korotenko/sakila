import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('.env')

_client = MongoClient(os.getenv("MONGO_URI"))

def get_mongo_collection():
    return _client["MONGO_DB"]["MONGO_COLLECTION"]


def close_connection():
    _client.close()

