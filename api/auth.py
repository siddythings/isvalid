# auth.py
from api.common.response_handler import ResponseHandler
from api.common.http_status_codes import HTTPStatusCode
from datetime import datetime
from functools import wraps
from flask import request, jsonify, g
from jose import JWTError, jwt
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from datetime import datetime, timedelta
from api.settings.mongo import IsValidDB, users_collection
from bson.objectid import ObjectId
from pytz import utc

# Configuration
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
GOOGLE_CLIENT_ID = "357210261141-o50hol8icikb8hrol7f4v5krn2alf6uq.apps.googleusercontent.com"
ACCESS_TOKEN_EXPIRE_MINUTES = 50000

# Function to verify JWT token


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise Exception("Invalid token")
        return email
    except JWTError:
        raise Exception("Invalid token")

# Function to verify Google token


def verify_google_token(token):
    try:
        id_info = google_id_token.verify_oauth2_token(
            token, google_requests.Request(), GOOGLE_CLIENT_ID)
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Wrong issuer.')
        return id_info
    except ValueError as e:
        print(str(e))
        return None

# Function to create access token


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Decorator for token authentication


def authenticate_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        if not authorization:
            return ResponseHandler.error(
                HTTPStatusCode.UNAUTHORIZED, message="Token is missing"
            )
            # return {"detail": "Token is missing"}
        try:
            token_type, token = authorization.split(" ")
            if token_type.lower() != "bearer":
                return ResponseHandler.error(
                    HTTPStatusCode.UNAUTHORIZED, message="Invalid token type"
                )
            email = verify_token(token)
        except Exception as e:
            return ResponseHandler.error(
                HTTPStatusCode.UNAUTHORIZED, message=str(e)
            )

        user_details = IsValidDB.users.find_one({'email': email})
        if not user_details:
            return ResponseHandler.error(
                HTTPStatusCode.NOT_FOUND, message="User not found"
            )

        # Attach user info to Flask's `g` object
        g.email = email
        g.id = user_details.get("id")
        g.full_name = user_details.get("name")
        g.mobile = user_details.get("phone")
        g.selected_template = user_details.get("selected_template", None)
        return f(*args, **kwargs)
    return decorated

# Decorator for aadhar_amount_check (if needed)


def aadhar_amount_check(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        if not authorization:
            return jsonify({"detail": "Token is missing"}), 401
        try:
            token_type, token = authorization.split(" ")
            if token_type.lower() != "bearer":
                return jsonify({"detail": "Invalid token type"}), 401
            email = verify_token(token)
        except Exception as e:
            return jsonify({"detail": str(e)}), 401

        # Attach email to Flask's `g` object
        g.email = email
        g.username = email
        return f(*args, **kwargs)
    return decorated

# Function to check and insert email from Google token


def check_and_insert_email(token_info):
    existing_email = IsValidDB.users.find_one(
        {"email": token_info.get("email")}, {'_id': 0})

    if existing_email:
        print("Email already exists in the database.")
        return existing_email
    else:
        # Insert the email into the collection
        new_user_object_id = ObjectId()
        token_info['_id'] = new_user_object_id
        token_info['id'] = str(new_user_object_id)
        user_obj = {
            "_id": new_user_object_id,
            "id": str(new_user_object_id),
            "name": token_info.get("name"),
            "email": token_info.get("email"),
            "username": token_info.get("email").split("@")[0],
            "profile_picture": token_info.get("picture"),
            "password": "",  # You might want to handle password differently for Google users
            # Assuming you have these fields
            "city": token_info.get("city", ""),
            "website": token_info.get("website", ""),
            "phone": token_info.get("phone", ""),
            "currency": "USD",
            "created_at": datetime.now(utc).isoformat(),
            "updated_at": datetime.now(utc).isoformat()
        }
        users_collection.insert_one(user_obj)

        wallet_data = {
            "user_id": new_user_object_id,
            "balance": 0.0,
            "earnings": 0.0,
            "withdraw": 0.0,
            "created_at": datetime.now(utc).isoformat(),
            "updated_at": datetime.now(utc).isoformat(),
        }
        result = wallets_collection.insert_one(wallet_data)
        print("Email inserted into the database.")
    user_obj.pop('_id')
    return user_obj
# Decorator for token authentication


def get_user_details_from_username(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        username = kwargs.get("username")
        if not username:
            return ResponseHandler.error(
                HTTPStatusCode.UNAUTHORIZED, message="Username is missing"
            )

        user_details = IsValidDB.users.find_one({'username': username})

        if not user_details:
            return ResponseHandler.error(
                HTTPStatusCode.NOT_FOUND, message="User not found"
            )

        # Attach user info to Flask's `g` object
        g.username = username
        g.id = user_details.get("id")
        g.full_name = user_details.get("name")
        g.mobile = user_details.get("phone")
        g.selected_template = user_details.get("selected_template", None)
        return f(*args, **kwargs)
    return decorated


def authenticate_courses_users_token(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        authorization = request.headers.get("Authorization")
        if not authorization:
            return ResponseHandler.error(
                HTTPStatusCode.UNAUTHORIZED, message="Token is missing"
            )
            # return {"detail": "Token is missing"}
        try:
            token_type, token = authorization.split(" ")
            if token_type.lower() != "bearer":
                return ResponseHandler.error(
                    HTTPStatusCode.UNAUTHORIZED, message="Invalid token type"
                )
            email = verify_token(token)
        except Exception as e:
            return ResponseHandler.error(
                HTTPStatusCode.UNAUTHORIZED, message=str(e)
            )

        user_details = IsValidDB.courses_users.find_one({'email': email})
        if not user_details:
            return ResponseHandler.error(
                HTTPStatusCode.NOT_FOUND, message="User not found"
            )

        # Attach user info to Flask's `g` object
        g.email = email
        g.id = user_details.get("id")
        g.full_name = user_details.get("name")
        g.mobile = user_details.get("phone")
        g.courses_ids = user_details.get("courses_ids")
        g.selected_template = user_details.get("selected_template", None)
        return f(*args, **kwargs)
    return decorated
