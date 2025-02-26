from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from .resources.shopping_cart_resources import ShoppingCartResource,WishlistResource

shopping_cart_item=Blueprint('shopping_cart_item',__name__,url_prefix='/shopping_cart')

@shopping_cart_item.route('/add',methods=['POST'])
@jwt_required()
def shopping_cart_item_create():
    return ShoppingCartResource.post()

@shopping_cart_item.route('/all',methods=['GET'])
@jwt_required()
def shopping_cart_list():
    return ShoppingCartResource.get()

@shopping_cart_item.route('/put/<int:item_id>',methods=['PUT'])
@jwt_required()
def shopping_cart_update(item_id):
    return ShoppingCartResource.put(item_id)

@shopping_cart_item.route('/remove/<int:item_id>',methods=['DELETE'])
@jwt_required()
def shopping_cart_delete(item_id):
    return ShoppingCartResource.delete(item_id)


wishlist_bp=Blueprint('wishlist',__name__,url_prefix='/wishlist')

@wishlist_bp.route('/all', methods=['GET'])
@jwt_required()
def get_wishlist():
    return WishlistResource.get()

@wishlist_bp.route('/new', methods=['POST'])
@jwt_required()
def add_to_wishlist():
    return WishlistResource.post()

@wishlist_bp.route('/delete/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_from_wishlist(item_id):
    return WishlistResource.delete(item_id)