""" User related views """
from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import IntegrityError
from silver_app.utils.errors import ConflictException
from silver_app.utils.responses import success_response_decorator
from silver_app.utils.auth import AuthService
from silver_app.database import db
""" from silver_app.utils.errors import 
 """
from .models import User
from .serializers import user_schema


blueprint = Blueprint("user", __name__)



@blueprint.route("/api/user/register", methods=["POST"])
@use_kwargs(user_schema)
@success_response_decorator("User registered successfully", status_code=201)
def user_register(username, password, email, **kwargs):
    user, access_token = AuthService.register_user(username, email, password, **kwargs)

    user_data = user_schema.dump(user)

    cookies = AuthService.create_auth_cookies(access_token)

    return (user_data, {}, cookies)



@blueprint.route('/api/user/login', methods=['POST'])
@use_kwargs(user_schema)
@success_response_decorator("Login successful", status_code=200)
def login_user(username, password, **kwargs):

    user, access_token = AuthService.login_user(username, password, **kwargs)

    user_data = user_schema.dump(user)

    cookies = AuthService.create_auth_cookies(access_token)

    return (user_data, {}, cookies)


@blueprint.route('/api/user', methods=['GET'])
@jwt_required()
@success_response_decorator("User retrieval success", status_code=200)
def get_user():


    user_id = get_jwt_identity()

    user = User.get_by_id(user_id)
    
    user_data = user_schema.dump(user)

    print(user_data, {})
    return (user_data, {})

"""     user = current_user
    user.token = request.headers.environ['HTTP_AUTHORIZATION'].split('Token ')[1]
    return current_user """