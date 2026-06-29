from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
import pymongo

class Database:
    client: AsyncIOMotorClient = None
    db = None

    @classmethod
    def connect(cls):
        cls.client = AsyncIOMotorClient(settings.MONGO_URI)
        cls.db = cls.client[settings.DB_NAME]
        print("Connected to MongoDB (Async)")

    @classmethod
    def disconnect(cls):
        if cls.client:
            cls.client.close()
            print("Disconnected from MongoDB (Async)")

    @classmethod
    def get_db(cls):
        return cls.db

# For sync operations like import script, we might need a sync client
def get_sync_db():
    client = pymongo.MongoClient(settings.MONGO_URI)
    return client[settings.DB_NAME]
