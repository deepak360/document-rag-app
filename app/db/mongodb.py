from pymongo import MongoClient
from pymongo.database import Database

from app.core.config import settings

class MongoDB:
    client: MongoClient = None
    db: Database = None

mongodb = MongoDB()

def get_mongodb() -> Database:
    """
    Get MongoDB database connection
    """
    return mongodb.db

def connect_to_mongo():
    """
    Connect to MongoDB
    """
    mongodb.client = MongoClient(settings.MONGODB_URL)
    mongodb.db = mongodb.client[settings.MONGODB_DB_NAME]
    print("Connected to MongoDB")

def close_mongo_connection():
    """
    Close MongoDB connection
    """
    if mongodb.client:
        mongodb.client.close()
        print("MongoDB connection closed")