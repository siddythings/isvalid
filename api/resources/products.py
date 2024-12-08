from flask import request, g
from flask_restful import Resource
from bson.objectid import ObjectId
from api.services.products import ProductService, QRService
from api.settings.mongo import products_collection
from api.common.helpper_function import method_not_allowed
from api.common.response_handler import ResponseHandler
from api.common.http_status_codes import HTTPStatusCode
from pydantic import ValidationError
from api.auth import (
    authenticate_token,
    get_user_details_from_username
)

from datetime import datetime
from pytz import utc


class CreateProductResource(Resource):
    # @authenticate_token
    def post(self):
        user_id = "g.id"

        requested_data = request.get_json()
        new_product = ProductService.create_product(requested_data, user_id)
        return ResponseHandler.success(data=new_product, message="Product created")

    # This will prevent other HTTP methods from being accepted on this route
    method_decorators = {'get': [method_not_allowed],
                         'put': [method_not_allowed],
                         'delete': [method_not_allowed]}


class ProductResource(Resource):
    # @authenticate_token
    def get(self, product_id=None):
        # Fetch all products if no ID is provided
        user_id = "g.id"

        if product_id is None:
            all_products = ProductService.get_products_by_user_id(
                user_id=user_id)
            return ResponseHandler.success(data=all_products, message="Products")

        # Fetch a single product by product_id
        try:
            product = ProductService.get_product_by_id(
                user_id=user_id, product_id=product_id)
            if product:
                # product['_id'] = str(product['_id'])
                return ResponseHandler.success(data=product, message="Products")
            return ResponseHandler.error(HTTPStatusCode.NOT_FOUND, message="Product not found")
        except:
            return ResponseHandler.error(HTTPStatusCode.BAD_REQUEST, message='Invalid product ID')

    # @authenticate_token
    def put(self, product_id):
        # Update an existing product
        user_id = "g.id"

        requested_data = request.get_json()
        try:
            result = ProductService.update_product_by_id(
                user_id=user_id, product_id=product_id, product_object=requested_data)
            if result:
                updated_product = ProductService.get_product_by_id(
                    user_id=user_id, product_id=product_id)
                return ResponseHandler.success(data=updated_product, message="Product updated")
            return ResponseHandler.error(HTTPStatusCode.NOT_FOUND, message="Product not found")
        except:
            return ResponseHandler.error(HTTPStatusCode.BAD_REQUEST, 'Invalid product ID')

    # @authenticate_token
    def delete(self, product_id):
        # Delete a product by ID
        user_id = "g.id"
        try:
            result = ProductService.delete_product_by_id(
                user_id=user_id, product_id=product_id)
            if result:
                return ResponseHandler.success(message="Product deleted")
            return ResponseHandler.error(HTTPStatusCode.NOT_FOUND, message="Product not found")
        except:
            return ResponseHandler.error(HTTPStatusCode.BAD_REQUEST, 'Invalid product ID')


class CreateQRProductResource(Resource):
    # @authenticate_token
    def post(self):
        user_id = "g.id"

        requested_data = request.get_json()
        product_id = requested_data.get("product_id")
        if not product_id:
            return ResponseHandler.error(HTTPStatusCode.NOT_FOUND, message="Product ID not found")

        qr_details = requested_data.get("requested_data", {})
        new_product = QRService.create_product_qr(
            qr_details, product_id, user_id)
        return ResponseHandler.success(data=new_product, message="Product created")

    # This will prevent other HTTP methods from being accepted on this route
    method_decorators = {'get': [method_not_allowed],
                         'put': [method_not_allowed],
                         'delete': [method_not_allowed]}


class ProductQRResource(Resource):
    # @authenticate_token
    def get(self, product_id=None):
        # Fetch all products if no ID is provided
        user_id = "g.id"

        all_products = QRService.get_products_qr(
            product_id=product_id)
        return ResponseHandler.success(data=all_products, message="Products")

    # # @authenticate_token
    # def put(self, product_id):
    #     # Update an existing product
    #     user_id = "g.id"

    #     requested_data = request.get_json()
    #     try:
    #         result = ProductService.update_product_by_id(
    #             user_id=user_id, product_id=product_id, product_object=requested_data)
    #         if result:
    #             updated_product = ProductService.get_product_by_id(
    #                 user_id=user_id, product_id=product_id)
    #             return ResponseHandler.success(data=updated_product, message="Product updated")
    #         return ResponseHandler.error(HTTPStatusCode.NOT_FOUND, message="Product not found")
    #     except:
    #         return ResponseHandler.error(HTTPStatusCode.BAD_REQUEST, 'Invalid product ID')

    # @authenticate_token
    def delete(self, product_id):
        # Delete a product by ID
        user_id = "g.id"
        try:
            result = QRService.delete_product_qr_by_id(
                user_id=user_id, product_id=product_id)
            if result:
                return ResponseHandler.success(message="Product deleted")
            return ResponseHandler.error(HTTPStatusCode.NOT_FOUND, message="Product not found")
        except:
            return ResponseHandler.error(HTTPStatusCode.BAD_REQUEST, 'Invalid product ID')
