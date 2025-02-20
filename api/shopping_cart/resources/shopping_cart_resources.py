from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models.shopping_cart_item import ShoppingCartItem
from models.shopping_cart import ShoppingCart
from models.wishlist_item import WishlistItem
from models.product_item import ProductItem
from ..schemas.shopping_cart_schema import ShoppingCartItemSchema
from ..schemas.wishlist_schema import WishListSchema
from flask_jwt_extended import  get_jwt_identity


class ShoppingCartResource(Resource):
    def get():
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401
        
        user_cart = ShoppingCart.query.filter_by(user_id=current_user['user_id']).first()
        if not user_cart:
            return jsonify({'message': 'Shopping cart not found'}), 404
        
        cart_items = ShoppingCartItem.query.filter_by(cart_id=user_cart.id).all()
        cartItemSchema = ShoppingCartItemSchema(many=True)
        return cartItemSchema.jsonify(cart_items),200

    def post():
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401
        
        user_cart = ShoppingCart.query.filter_by(user_id=current_user['user_id']).first()
        if not user_cart:
            return jsonify({'message': 'Shopping cart not found'}), 404
        data = request.get_json()
        product_item_id = data.get('product_item_id')
        if not product_item_id:
            return jsonify({'message': 'Product item ID is required'}), 400
        
        product = ProductItem.query.get(product_item_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        new_item = ShoppingCartItem(
            cart_id=user_cart.user_id,
            product_item_id=data.get('product_item_id'),
            qty=data.get('qty')
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item added to cart', 'id': new_item.id})

    def put(item_id):
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401
        user_cart = ShoppingCart.query.filter_by(user_id=current_user['user_id']).first()
        if not user_cart:
            return jsonify({'message': 'Shopping cart not found'}), 404
        data = request.get_json()
        item = ShoppingCartItem.query.filter_by(id=item_id,cart_id=user_cart.id).first()
        if not item:
            return jsonify({'message': 'Item not found'}), 404
        
        item.qty = data.get('qty', item.qty)  # Update quantity if provided
        db.session.commit()
        return jsonify({'message': 'Item updated successfully'})

    def delete(item_id):
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401
        user_cart = ShoppingCart.query.filter_by(user_id=current_user['user_id']).first()
        if not user_cart:
            return jsonify({'message': 'Shopping cart not found'}), 404
        item = ShoppingCartItem.query.filter_by(id=item_id,cat_id=user_cart.id).first()
        if not item:
            return jsonify({'message': 'Item not found'}), 404
        
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})


class WishlistResource:

    def get():
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401

        user_cart = ShoppingCart.query.filter_by(user_id=current_user['user_id']).first()
        if not user_cart:
            return jsonify({'message': 'Shopping cart not found'}), 404
        wishListSchema= WishListSchema(many=True)
        wishlist_items = WishlistItem.query.filter_by(cart_id=user_cart.id).all()
        return jsonify(wishListSchema.dump(wishlist_items)), 200

    def post():
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401

        user_cart = ShoppingCart.query.filter_by(user_id=current_user['user_id']).first()
        if not user_cart:
            return jsonify({'message': 'Shopping cart not found'}), 404

        data = request.get_json()
        product_item_id = data.get('product_item_id')
        if not product_item_id:
            return jsonify({'message': 'Product item ID is required'}), 400

        # Check if product exists
        product = ProductItem.query.get(product_item_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        # Check if item already in wishlist
        existing_item = WishlistItem.query.filter_by(cart_id=user_cart.id, product_item_id=product_item_id).first()
        if existing_item:
            return jsonify({'message': 'Item already in wishlist'}), 409

        new_wishlist_item = WishlistItem(cart_id=user_cart.id, product_item_id=product_item_id)

        db.session.add(new_wishlist_item)
        db.session.commit()

        return jsonify({'message': 'Item added to wishlist', 'id': new_wishlist_item.id}), 201

    def delete(item_id):
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401

        user_cart = ShoppingCart.query.filter_by(user_id=current_user['user_id']).first()
        if not user_cart:
            return jsonify({'message': 'Shopping cart not found'}), 404

        item = WishlistItem.query.filter_by(id=item_id, cart_id=user_cart.id).first()
        if not item:
            return jsonify({'message': 'Item not found in wishlist'}), 404

        db.session.delete(item)
        db.session.commit()

        return jsonify({'message': 'Item removed from wishlist'}), 200

