import os
import jsons
import base64
import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from bson.objectid import ObjectId
from settings.mongo import products_collection, payment_orders_collection


class PhonePePaymentGateway:
    URI = "https://api.phonepe.com/apis/hermes/pg/v1/pay"
    merchantId = os.getenv("PHONEPE_MERCHANTID")
    INDEX = os.getenv("PHONEPE_INDEX")
    ENDPOINT = os.getenv("PHONEPE_ENDPOINT")
    SALTKEY = os.getenv("PHONEPE_SALTKEY")

    @staticmethod
    def calculate_sha256_string(input_string):
        # Create a hash object using the SHA-256 algorithm
        sha256 = hashes.Hash(hashes.SHA256(), backend=default_backend())
        # Update hash with the encoded string
        sha256.update(input_string.encode('utf-8'))
        # Return the hexadecimal representation of the hash
        return sha256.finalize().hex()

    @staticmethod
    def base64_encode(input_dict):
        # Convert the dictionary to a JSON string
        json_data = jsons.dumps(input_dict)
        # Encode the JSON string to bytes
        data_bytes = json_data.encode('utf-8')
        # Perform Base64 encoding and return the result as a string
        return base64.b64encode(data_bytes).decode('utf-8')

    @staticmethod
    def create_check_sum(base64String):

        mainString = base64String + PhonePePaymentGateway.ENDPOINT + \
            PhonePePaymentGateway.SALTKEY
        sha256Val = PhonePePaymentGateway.calculate_sha256_string(mainString)
        checkSum = sha256Val + '###' + PhonePePaymentGateway.INDEX
        return checkSum

    @staticmethod
    def create_payload(amount, transaction_id, user_id):
        payload = {
            "merchantId": PhonePePaymentGateway.merchantId,
            "merchantTransactionId": transaction_id,
            "merchantUserId": user_id,
            "amount": amount,
            "redirectUrl": os.getenv("PHONEPE_REDIRECTURL"),
            "redirectMode": "REDIRECT",
            "callbackUrl": os.getenv("PHONEPE_CALLBACKURL"),
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }
        insert_payload = payload.copy()
        insert_payload.update({
            '_id': ObjectId(transaction_id)
        })
        payment_orders_collection.insert_one(insert_payload)
        return payload

    @staticmethod
    def get_product_user_id(product_id):
        products_object = products_collection.find_one({'id': product_id}, {
            'user_id': 1,
            '_id': 0
        })
        if products_object:
            return products_object.get("user_id")
        else:
            raise ("Unable Get Product User ID")

    @staticmethod
    def payment_request(amount, product_id):
        object_id = ObjectId()
        user_id = PhonePePaymentGateway.get_product_user_id(product_id)
        transaction_id = str(object_id)
        payload = PhonePePaymentGateway.create_payload(
            amount, transaction_id, user_id)
        base64String = PhonePePaymentGateway.base64_encode(payload)

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "X-VERIFY": PhonePePaymentGateway.create_check_sum(base64String)
        }
        json_data = {
            'request': base64String,
        }
        response = requests.post(
            PhonePePaymentGateway.URI, json=json_data, headers=headers)

        return response.json()
