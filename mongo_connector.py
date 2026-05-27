import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv('.env')



def get_mongo_collection():
    client = MongoClient(os.getenv('MONGO_URI'))
    db = client["ich_edit"]
    return db["final_project_121225ptm_Kateryna"]




