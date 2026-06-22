from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def get_mongo_client():
    client = MongoClient(os.getenv("MONGODB_URL"))
    return client

def get_mongo_db():
    client = get_mongo_client()
    db = client[os.getenv("MONGODB_DB_NAME")]
    return db

if __name__ == "__main__":
    db = get_mongo_db()
    print(f"✅ Connected to MongoDB: {db.name}")