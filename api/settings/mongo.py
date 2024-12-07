import pymongo
import os

from dotenv import load_dotenv
load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('DB_NAME')
client = pymongo.MongoClient(MONGODB_URI)
IsValidDB = client[DB_NAME]

# Links collection
users_collection = IsValidDB.users
products_collection = IsValidDB.products
