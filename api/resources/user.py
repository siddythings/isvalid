from flask import Flask, jsonify, request, g
from flask_restful import Resource, Api
from api.auth import (
    authenticate_token,
    verify_google_token,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    check_and_insert_email,
)
from bson.objectid import ObjectId
from datetime import timedelta
from api.settings.mongo import LnkrDB
from api.common.response_handler import ResponseHandler
from api.common.http_status_codes import HTTPStatusCode
from api.models.users import Users as UsersModel
from datetime import datetime
from pytz import utc
import random


class UserProfile(Resource):
    @authenticate_token
    def get(self):
        # Get profile by token email
        email = g.email
        user = UsersModel.get_user_by_email(email=email)
        if user is None:
            return ResponseHandler.error(
                HTTPStatusCode.NOT_FOUND, message="User not found"
            )
        return ResponseHandler.success(data=user, message="User details")

    @authenticate_token
    def patch(self):
        # Update user profile by token email
        email = g.email
        data = request.json
        if not data:
            return ResponseHandler.error(
                HTTPStatusCode.BAD_REQUEST, message="Payload not found"
            )

        UsersModel.update_user_by_email(email=email, user_object=data)

        user = UsersModel.get_user_by_email(email=email)
        return ResponseHandler.success(data=user, message="User details updated")


class GoogleLogin(Resource):
    def post(self):
        data = request.json
        if not data or "credential" not in data:
            return ResponseHandler.error(
                HTTPStatusCode.NOT_FOUND, message="No data provided"
            )

        credential = data["credential"]
        token_info = verify_google_token(credential)
        if not token_info:
            return ResponseHandler.error(
                HTTPStatusCode.NOT_FOUND, message="Token is invalid!"
            )

        user_obj = check_and_insert_email(token_info)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": token_info["email"]}, expires_delta=access_token_expires
        )
        return ResponseHandler.success(
            data={
                "access_token": access_token,
                "token_type": "bearer",
                "user": user_obj
            },
            message="Google auth",
        )


class RegisterUser(Resource):
    def post(self):
        data = request.json
        name = data.get("name")
        password = data.get("password")
        email = data.get("email")

        user = UsersModel.get_user_by_email(email=email)
        if user:
            return ResponseHandler.error(
                HTTPStatusCode.CONFLICT, message="User already exists"
            )

        new_user_object_id = ObjectId()

        user_obj = {
            "_id": new_user_object_id,
            "id": str(new_user_object_id),
            "name": name,
            "email": email,
            "username": email.split("@")[0] + str(random.randint(1, 1000)),
            "password": password,
            "created_at": datetime.now(utc).isoformat(),
            "updated_at": datetime.now(utc).isoformat(),
            "currency": "USD"
        }
        UsersModel.insert_user(user_object=user_obj)

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": email}, expires_delta=access_token_expires
        )
        return ResponseHandler.success(
            data={"access_token": access_token, "token_type": "bearer"},
            message="User Register Done",
        )


class LoginUser(Resource):
    def post(self):
        data = request.json
        email = data.get("email")
        password = data.get("password")

        user = LnkrDB.users.find_one({"email": email})
        if user and user["password"] == password:
            access_token_expires = timedelta(
                minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(
                data={"sub": user["email"]}, expires_delta=access_token_expires
            )
            return ResponseHandler.success(
                data={"access_token": access_token, "token_type": "bearer"},
                message="User Login Done",
            )
        return ResponseHandler.error(
            HTTPStatusCode.UNAUTHORIZED, message="Invalid email or password"
        )


class UsernameAvailability(Resource):
    def get(self, username):
        """Check if the username is available"""
        user = UsersModel.get_user_by_username_v2(username=username)
        if user:
            return ResponseHandler.error(
                HTTPStatusCode.BAD_REQUEST,
                message=f"Username '{username}' is already taken.",
            )
        return ResponseHandler.success(message=f"Username '{username}' is available.")


class UpdateUsername(Resource):
    @authenticate_token
    def put(self):
        """Update an existing username"""
        data = request.json

        user_id = g.id
        old_username = data.get("old_username")
        new_username = data.get("username")

        if UsersModel.get_user_by_username(user_id, new_username):
            return ResponseHandler.error(
                HTTPStatusCode.BAD_REQUEST,
                message=f"Username '{new_username}' is already taken.",
            )

        if UsersModel.update_username(user_id, old_username, new_username):
            return ResponseHandler.success(
                message=f"Username updated to '{new_username}'"
            )
        return ResponseHandler.success(message=f"User '{old_username}' not found.")
