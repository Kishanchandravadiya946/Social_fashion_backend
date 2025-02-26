from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models.shopping_cart_item import ShoppingCartItem
from models.shopping_cart import ShoppingCart
from models.wishlist_item import WishlistItem
from models.product_item import ProductItem
from models.product import Product
from ..schemas.shopping_cart_schema import ShoppingCartItemSchema
from ..schemas.wishlist_schema import WishListSchema
from flask_jwt_extended import get_jwt_identity


class ShoppingCartResource(Resource):
    def get():
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401

        user_cart = ShoppingCart.query.filter_by(
            user_id=current_user['user_id']).first()
        if not user_cart:
            return jsonify({'message': 'Shopping cart not found'}), 404

        cart_items = ShoppingCartItem.query.filter_by(
            cart_id=user_cart.id).all()
        
        cart_product_tuples = [
            (item.id, item.product_item_id, item.qty) for item in cart_items]
        # print(cart_product_tuples)
        if not cart_product_tuples:
          return jsonify({"message": "No products found in the cart"}), 404

        product_ids = [item[1] for item in cart_product_tuples]
 
        product_items = db.session.query(
             ProductItem.id,
             ProductItem.SKU,
              ProductItem.qty_in_stock,
              ProductItem.product_image,
              ProductItem.price,
               ProductItem.product_id,
          Product.name.label("product_name"),
         Product.description.label("product_description")
         ).join(Product, ProductItem.product_id == Product.id).filter(ProductItem.id.in_(product_ids)).all()
        # print(product_items)
        cart_map = {product_id: (cart_item_id, qty)
                for cart_item_id, product_id, qty in cart_product_tuples}
        # print(cart_map)
        result = [
        {
            "cart_item_id": cart_map[item.id][0],  
            "id": item.id,  
            "SKU": item.SKU,
            "qty_in_stock": item.qty_in_stock,
            "product_image": item.product_image,
            "price": item.price,
            "product_id": item.product_id,
            "product_name": item.product_name,
            "product_description": item.product_description,
            "qty": cart_map[item.id][1]  
        }
          for item in product_items
        ]
        # print(result) 
        return jsonify({"cart_product_items": result}), 200

    def post():
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401

        user_cart = ShoppingCart.query.filter_by(
            user_id=current_user['user_id']).first()
        if not user_cart:
            return jsonify({'message': 'Shopping cart not found'}), 404
        data = request.get_json()
        product_item_id = data.get('product_item_id')
        if not product_item_id:
            return jsonify({'message': 'Product item ID is required'}), 400

        product = ProductItem.query.get(product_item_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        existing_cart_item = ShoppingCartItem.query.filter_by(
            cart_id=user_cart.id, product_item_id=product_item_id).first()
        # print(data.get('qty'))
        
        if existing_cart_item:
            if existing_cart_item.qty == 5 and not data.get('qty'):
                return jsonify({'message': 'You already reach the limit'}), 400
            if data.get('qty'):
                existing_cart_item.qty = data.get('qty', 1)
            else :
                existing_cart_item.qty+=1
            print(existing_cart_item.qty)
            db.session.commit()
            return jsonify({'message': 'Product quantity updated in cart'})
        
        new_item = ShoppingCartItem(
            cart_id=user_cart.id,
            product_item_id=data.get('product_item_id'),
            qty=data.get('qty', 1)
        )
        db.session.add(new_item)
        db.session.commit()
        return jsonify({'message': 'Item added to cart', 'id': new_item.id})

    def put(item_id):
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401
        user_cart = ShoppingCart.query.filter_by(
            user_id=current_user['user_id']).first()
        if not user_cart:
            return jsonify({'message': 'Shopping cart not found'}), 404
        data = request.get_json()
        item = ShoppingCartItem.query.filter_by(
            id=item_id, cart_id=user_cart.id).first()
        if not item:
            return jsonify({'message': 'Item not found'}), 404

        item.qty = data.get('qty', item.qty)  # Update quantity if provided
        db.session.commit()
        return jsonify({'message': 'Item updated successfully'})

    def delete(item_id):
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401
        user_cart = ShoppingCart.query.filter_by(
            user_id=current_user['user_id']).first()
        if not user_cart:
            return jsonify({'message': 'Shopping cart not found'}), 404
        item = ShoppingCartItem.query.filter_by(
            id=item_id,cart_id=user_cart.id).first()
        # print(current_user['user_id'],item_id,user_cart.id,item)
        if not item:
            return jsonify({'message': 'Item not found'}), 404

        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'}),200


class WishlistResource:

    def get():
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401

        user_cart = ShoppingCart.query.filter_by(
            user_id=current_user['user_id']).first()
        if not user_cart:
            return jsonify({'message': 'Shopping cart not found'}), 404
        wishlist_items = WishlistItem.query.filter_by(
            cart_id=user_cart.id).all()

        wishlist_product_tuples = [(item.id, item.product_item_id)
                                    for item in wishlist_items]


        if not wishlist_product_tuples:
            return jsonify({"message": "No products found in wishlist"}), 404

        product_ids = [item[1] for item in wishlist_product_tuples]

        product_items = db.session.query(
          ProductItem.id,
          ProductItem.SKU,
          ProductItem.qty_in_stock,
          ProductItem.product_image,
          ProductItem.price,
          ProductItem.product_id,
          Product.name.label("product_name"),
          Product.description.label("product_description")
        ).join(Product, ProductItem.product_id == Product.id).filter(ProductItem.id.in_(product_ids)).all()

        wishlist_map = {product_id: wishlist_id for wishlist_id,
        product_id in wishlist_product_tuples}

        result = [
          {
            "wishlist_id": wishlist_map[item.id], 
             "id": item.id,
             "SKU": item.SKU,
           "qty_in_stock": item.qty_in_stock,
            "product_image": item.product_image,
            "price": item.price,
           "product_id": item.product_id,
            "product_name": item.product_name,
            "product_description": item.product_description
         }
         for item in product_items
            ]

        return jsonify({"Wishlist_product_items": result}), 200

    def post():
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401

        user_cart = ShoppingCart.query.filter_by(
            user_id=current_user['user_id']).first()
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
        existing_item = WishlistItem.query.filter_by(
            cart_id=user_cart.id, product_item_id=product_item_id).first()
        if existing_item:
            return jsonify({'message': 'Item already in wishlist'}), 409

        new_wishlist_item = WishlistItem(
            cart_id=user_cart.id, product_item_id=product_item_id)

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
