from api.common.constants import ProductType
from api.settings.mongo import products_collection
from api.common.email_template import EamilTemplates, Email
from bson.objectid import ObjectId
from datetime import datetime
from pytz import utc


class ProductService:
    @staticmethod
    def get_product_details(product_id):
        return products_collection.find_one({"id": product_id})

    @staticmethod
    def create_product(product_data, user_id):
        object_id = ObjectId()

        product_data.update({
            '_id': object_id,
            'id': str(object_id),
            'user_id': user_id,
            "is_published": False,
            "is_deleted": False,
            "created_at":  datetime.now(utc).isoformat(),
            "updated_at": datetime.now(utc).isoformat()
        })
        products_collection.insert_one(product_data)
        product_data['_id'] = str(product_data['_id'])
        return product_data

    @staticmethod
    def update_product_by_id(product_data, product_id):

        product_data.update({
            "is_published": False,
            "is_deleted": False,
            "updated_at": datetime.now(utc).isoformat()
        })
        products_collection.update_one(
            {'id': product_id}, {"$set": product_data})
        return product_data

    @staticmethod
    def get_products_by_user_id(user_id):
        all_products = products_collection.find(
            {'user_id': user_id, "is_deleted": False}, {'_id': 0})
        return list(all_products)

    @staticmethod
    def get_product_by_id(product_id, user_id):
        product_obj = products_collection.find_one(
            {'user_id': user_id, 'id': product_id}, {'_id': 0})
        return product_obj

    @staticmethod
    def delete_product_by_id(product_id, user_id):
        product_data = {
            "is_deleted": True,
            "updated_at": datetime.now(utc).isoformat()
        }
        products_collection.update_one(
            {'id': product_id, 'user_id': user_id}, {"$set": product_data})

        return product_data
