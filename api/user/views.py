from flask import Blueprint
from .resources.user_resource import UserResource

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/create', methods=['POST'])
def create_user():
    return UserResource.create_user()

@user_bp.route('/list', methods=['GET'])
def get_users():
    return UserResource.get_users()

@user_bp.route('/login',methods=['POST'])
def login_user():
    return UserResource.login_user()