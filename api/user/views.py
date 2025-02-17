from flask import Blueprint
from .resources.user_resource import UserResource
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/create', methods=['POST'])
def create_user():
    return UserResource.create_user()

@user_bp.route('/list', methods=['GET'])
@jwt_required()
def get_users():
    return UserResource.get_users()

@user_bp.route('/login',methods=['POST'])
def login_user():
    return UserResource.login_user()

@user_bp.route('/logout',methods=['POST'])
@jwt_required()
def logout_user():
    return UserResource.logout_user()

@user_bp.route('profile',methods=['GET'])
@jwt_required()
def get_profile():
    return UserResource.get_profile()
