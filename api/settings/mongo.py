import pymongo
import os

from dotenv import load_dotenv
load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
DB_NAME = os.getenv('DB_NAME')
client = pymongo.MongoClient(MONGODB_URI)
LnkrDB = client[DB_NAME]

# Links collection
links_collection = LnkrDB.links
users_collection = LnkrDB.users
products_collection = LnkrDB.products
availability_calendar_collection = LnkrDB.calendar_availability
courses_collection = LnkrDB.courses
profile_templates_collection = LnkrDB.profile_templates
products_ordering_list_collection = LnkrDB.products_ordering_list
user_calendar_connection = LnkrDB.user_calendar_connection
product_orders_collection = LnkrDB.product_orders
courses_users_collection = LnkrDB.courses_users
users_audience_collection = LnkrDB.users_audience
payment_orders_collection = LnkrDB.payment_orders
orders_collection = LnkrDB.orders
wallets_collection = LnkrDB.wallets
