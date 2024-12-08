from api.common.constants import ProductType
from api.settings.mongo import products_collection, qrcode_collection
from api.common.email_template import EamilTemplates, Email
from bson.objectid import ObjectId
from datetime import datetime
from pytz import utc
# import qrcode
import os
# from qrcode.image.styledpil import StyledPilImage
# from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
# from qrcode.image.styles.colormasks import RadialGradiantColorMask
from dotenv import load_dotenv

load_dotenv()


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
            {'user_id': user_id, "is_deleted": False}, {'_id': 0}).sort({'_id': -1})
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


class QRService:
    # @staticmethod
    # def genrate_qr(product_id):
    #     QR_URL = f'{product_id}'
    #     # Create the QR code object with no border
    #     qr = qrcode.QRCode(
    #         error_correction=qrcode.constants.ERROR_CORRECT_H,
    #         border=0  # Set border to 0 to remove the border
    #     )
    #     qr.add_data('https://google.com')  # Add the URL data

    #     # Generate QR code with rounded module drawer
    #     img_1 = qr.make_image(image_factory=StyledPilImage,
    #                           module_drawer=RoundedModuleDrawer())
    #     img_1.save("qr_rounded_no_border.png")

    @staticmethod
    def create_product_qr(qr_details, product_id, user_id):
        object_id = ObjectId()
        URL = os.getenv("ISVALID_URL", 'https://google.com')
        QR_URL = f'{URL}/{str(object_id)}'
        qr_product_data = {
            '_id': object_id,
            'id': str(object_id),
            'qr_details': qr_details,
            'product_id': product_id,
            'user_id': user_id,
            'url': QR_URL,
            "is_published": False,
            "is_deleted": False,
            "created_at":  datetime.now(utc).isoformat(),
            "updated_at": datetime.now(utc).isoformat()
        }
        qrcode_collection.insert_one(qr_product_data)
        qr_product_data['_id'] = str(qr_product_data['_id'])
        return qr_product_data

    @staticmethod
    def get_products_qr(product_id):
        qr_product_data = qrcode_collection.find({
            "product_id": product_id,
        }, {'_id': 0}).sort({'_id': -1})
        return list(qr_product_data)

    @staticmethod
    def delete_product_qr_by_id(qr_id):
        product_data = {
            "is_deleted": True,
            "updated_at": datetime.now(utc).isoformat()
        }
        qr_product_data = qrcode_collection.update_one({
            "id": qr_id,
        }, {'$set': product_data})
        return list(qr_product_data)

    @staticmethod
    def get_product_details_by_qr_id(qr_id):
        data = qrcode_collection.find_one({
            'id': qr_id
        }, {'_id': 0})
        prduct = products_collection.find_one(
            {'id': data.get("product_id")}, {'_id': 0})
        data.update(
            prduct
        )
        return data
