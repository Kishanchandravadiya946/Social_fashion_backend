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

@user_bp.route('/profile',methods=['GET'])
@jwt_required()
def get_profile():
    return UserResource.get_profile()

@user_bp.route('/update',methods=['PUT'])
@jwt_required()
def update_profile():
    return UserResource.profile_update()


@user_bp.route('/new_address',methods=['POST'])
@jwt_required()
def create_address():
    return UserResource.address_create()

@user_bp.route('/get_countries',methods=['GET'])
@jwt_required()
def get_countries():
    return UserResource.get_countries()

@user_bp.route('/addresslist',methods=['GET'])
@jwt_required()
def get_address():
    # print("M")
    return UserResource.address_fetch()

@user_bp.route('/set-default-address/<int:address_id>',methods=['PUT'])
@jwt_required()
def set_address(address_id):
    # print(address_id)
    return UserResource.address_set(address_id)


@user_bp.route('/delete-address/<int:address_id>',methods=['DELETE'])
@jwt_required()
def delete_address(address_id):
    print(address_id)
    return UserResource.address_delete(address_id)








