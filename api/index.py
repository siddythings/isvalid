import os
from flask import Flask, send_from_directory
from flask_mail import Mail
from flask_restful import Api, Resource
from flask_cors import CORS
from dotenv import load_dotenv

from api.common.helpper_function import send_error_email
from api.common.response_handler import ResponseHandler
from api.common.http_status_codes import HTTPStatusCode

from api.routes.users import users_bp
from api.routes.products import product_bp
from api.routes.presigned_url import presigned_bp


# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)
# Set configurations from environment variables
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["DEBUG"] = False

# Configure Flask-Mail for Gmail
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USE_SSL"] = True

mail = Mail(app)

# Enable CORS for all routes
CORS(app)

# Initialize the API object
api = Api(app)


# app.register_blueprint(product_bp)
app.register_blueprint(users_bp)
app.register_blueprint(product_bp)
app.register_blueprint(presigned_bp)


@app.route("/")
def home():
    return "Hello, World!"


# Global 404 error handler
@app.errorhandler(404)
def not_found_error(error):
    return ResponseHandler.error(HTTPStatusCode.BAD_REQUEST, "Resource not found")


# Global 500 error handler
@app.errorhandler(500)
def handle_internal_server_error(e):
    """
    Handle all 500 errors and send an email alert with the error trace.
    """
    # Send an email with the error details
    send_error_email(mail, e)

    # Return a generic error response to the client
    return ResponseHandler.error(
        HTTPStatusCode.INTERNAL_SERVER_ERROR,
        "Internal Server Error",
        details={
            "error": "An internal server error occurred. The administrators have been notified."
        },
    )
