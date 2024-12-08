from flask import request, jsonify
from flask_restful import Resource
from bson.objectid import ObjectId
from api.common.helpper_function import method_not_allowed
from api.common.response_handler import ResponseHandler
from api.common.http_status_codes import HTTPStatusCode
import boto3
import os
from api.common.constants import FILE_EXTENSTIONS_MAPPING

from api.auth import authenticate_token

# Initialize the S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION_NAME"),
)

# Replace with your S3 bucket name
BUCKET_NAME = "isvalid"


class PresignedURLResource(Resource):

    def get_file_extension(self, filename):
        return os.path.splitext(filename)[1][1:]

    # @authenticate_token
    def post(self):
        """
        POST method to generate a presigned URL for S3 object
        """
        try:
            # Get the input data from the request body
            data = request.json
            bucket_name = BUCKET_NAME
            file_name = data.get("file_name")
            expiration = data.get("expiration", 3600)  # Default to 1 hour

            if not bucket_name or not file_name:
                return {"message": "bucket_name and object_name are required."}, 400

            # Generate the presigned URL
            presigned_url = s3_client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": BUCKET_NAME,
                    "Key": file_name,
                    "ContentType": FILE_EXTENSTIONS_MAPPING.get(
                        self.get_file_extension(file_name)
                    ),
                },
                ExpiresIn=expiration,
            )
            return ResponseHandler.success(
                data={
                    "presigned_url": presigned_url,
                    "url": f"https://isvalid.s3.amazonaws.com/{file_name}",
                },
                message="Presigned URL created",
            )
        except Exception as e:
            return ResponseHandler.error(
                HTTPStatusCode.INTERNAL_SERVER_ERROR,
                message="An unexpected error occurred: {}".format(str(e)),
            )

    # @authenticate_token
    def get(self):
        try:
            # Get the input data from the request body
            data = request.json
            bucket_name = BUCKET_NAME
            file_name = data.get("file_name")
            expiration = data.get("expiration", 3600)  # Default to 1 hour

            if not bucket_name or not file_name:
                return {"message": "bucket_name and object_name are required."}, 400

            # Generate the presigned URL
            presigned_url = s3_client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": BUCKET_NAME,
                    "Key": file_name,  # Specify the key of the PNG file
                },
                ExpiresIn=expiration,  # Set the expiration time in seconds
            )
            return ResponseHandler.success(
                data={"presigned_url": presigned_url}, message="Presigned URL created"
            )
        except Exception as e:
            return ResponseHandler.error(
                HTTPStatusCode.INTERNAL_SERVER_ERROR,
                message="An unexpected error occurred: {}".format(str(e)),
            )
