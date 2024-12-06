from flask import jsonify


class ResponseHandler:
    @staticmethod
    def success(data=None, message="Request completed successfully", total_count=None, page_number=None):
        response = {
            "status": "success",
            "message": message
        }
        if data is not None:
            if type(data) == list:
                response["data"] = list(data)
            else:
                response["data"] = dict(data)
        return dict(response), 200

    @staticmethod
    def error(code, message="Bad Request", error_type=None, details=None):
        response = {
            "status": "error",
            "error": {
                "code": code.value,
                "message": message
            }
        }
        if error_type is not None:
            response["error"]["type"] = error_type
        if details is not None:
            response["error"]["details"] = details
        return dict(response), code.value
