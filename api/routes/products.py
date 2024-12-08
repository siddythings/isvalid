
from flask import Blueprint
from flask_restful import Api
from api.resources.products import ProductResource, CreateProductResource, CreateQRProductResource, ProductQRResource

product_bp = Blueprint('product', __name__)
api = Api(product_bp)

api.add_resource(CreateProductResource, "/api/v1/product", methods=["POST"])
api.add_resource(
    ProductResource, "/api/v1/products", "/api/v1/product/<string:product_id>"
)
api.add_resource(CreateQRProductResource,
                 "/api/v1/create-qr", methods=["POST"])
api.add_resource(
    ProductQRResource, "/api/v1/qr/<string:product_id>")
