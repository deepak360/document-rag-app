from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from app.db.sql import Base, engine
from app.db.mongodb import connect_to_mongo, close_mongo_connection

def create_start_app_handler(app: FastAPI):
    """
    FastAPI startup event handler
    """
    async def start_app() -> None:
        # Create SQL tables
        try:
            Base.metadata.create_all(bind=engine)
            print("SQL tables created")
        except SQLAlchemyError as e:
            print(f"Error creating SQL tables: {e}")
        
        # Connect to MongoDB
        connect_to_mongo()
    
    return start_app

def create_stop_app_handler(app: FastAPI):
    """
    FastAPI shutdown event handler
    """
    async def stop_app() -> None:
        # Close MongoDB connection
        close_mongo_connection()
    
    return stop_app