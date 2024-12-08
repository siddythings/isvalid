
from flask import Blueprint
from flask_restful import Api
from api.resources.s3_resources import PresignedURLResource

presigned_bp = Blueprint('presigned', __name__)
api = Api(presigned_bp)

api.add_resource(PresignedURLResource, "/api/v1/upload")
