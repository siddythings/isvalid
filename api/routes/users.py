
from flask import Blueprint
from flask_restful import Api
from api.resources.user import (
    UserProfile,
    GoogleLogin,
    RegisterUser,
    LoginUser,
    UsernameAvailability,
    UpdateUsername,
)

users_bp = Blueprint('users', __name__)
api = Api(users_bp)

api.add_resource(UserProfile, "/api/auth/profile")
api.add_resource(GoogleLogin, "/api/auth/google/login")
api.add_resource(RegisterUser, "/api/auth/user/register")
api.add_resource(LoginUser, "/api/auth/user/login")
api.add_resource(UsernameAvailability, "/api/v1/user/check-username/<string:username>")
api.add_resource(UpdateUsername, "/api/v1/user/update-username")