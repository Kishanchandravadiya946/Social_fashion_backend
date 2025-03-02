from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models.product_item import ProductItem
from models.product import Product
from models.product_category import ProductCategory
from models.wishlist_item import WishlistItem
from models.shopping_cart import ShoppingCart
from models.variation import Variation
from models.variation_option import VariationOption
from models.product_configuration import ProductConfiguration
from ..schemas.product_item_schema import ProductItemSchema
from ...shared.uploadFile import uploadfile 
from ...shared.isAllowedFile import isAllowedFile
from flask_jwt_extended import jwt_required, get_jwt_identity


class ProductItemResource(Resource):

    def post():
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
            return jsonify({'error': 'Unauthorized access'}), 403 

        data = request.form
        product_id = data.get('product_id')
        SKU = data.get('SKU')
        qty_in_stock = data.get('qty_in_stock')
        price = data.get('price')
        size_option_id = data.get('size_option_id')  # Selected size variation option ID
        color_option_id = data.get('color_option_id')  # Selected color variation option ID
        product_image = None

        if not product_id or not SKU or qty_in_stock is None or price is None:
            return {"error": "product_id, SKU, qty_in_stock, and price are required"}, 400

        product = Product.query.get(product_id)
        if not product:
            return {"error": f"Product with id {product_id} does not exist"}, 404

        # Fetch category ID of the selected product
        category_id = product.category_id
        if not category_id:
            return {"error": "Product does not belong to any category"}, 400

        # Validate the provided variation options
        size_option = VariationOption.query.filter_by(id=size_option_id).first()
        color_option = VariationOption.query.filter_by(id=color_option_id).first()

        if not size_option or not color_option:
            return {"error": "Invalid variation options"}, 400

        # Validate that the selected variation options belong to the category variations
        size_variation = Variation.query.filter_by(id=size_option.variation_id, category_id=category_id).first()
        color_variation = Variation.query.filter_by(id=color_option.variation_id, category_id=category_id).first()

        if not size_variation or not color_variation:
            return {"error": "Selected variation options do not match the product category"}, 400

        # Handle product image upload
        if "product_image" in request.files:
            file = request.files["product_image"]
            if file.filename == "":
                return {"error": "No selected file"}, 400
            if not isAllowedFile(file):
                return {"error": "Invalid image format. Allowed formats: PNG, JPG, JPEG, GIF, BMP, WEBP"}, 400
            product_image = uploadfile(file, file.filename)

        # Create a new product item
        new_product_item = ProductItem(
            product_id=product_id,
            SKU=SKU,
            qty_in_stock=qty_in_stock,
            product_image=product_image,
            price=price
        )

        db.session.add(new_product_item)
        db.session.commit()

        # Create product configurations (size & color)
        size_config = ProductConfiguration(product_item_id=new_product_item.id, variation_option_id=size_option.id)
        color_config = ProductConfiguration(product_item_id=new_product_item.id, variation_option_id=color_option.id)

        db.session.add(size_config)
        db.session.add(color_config)
        db.session.commit()

        product_item_schema = ProductItemSchema()
        return {
            "message": "Product item created successfully",
            "product_item": product_item_schema.dump(new_product_item)
        }, 201




    def get():
       try:
         product_items = ProductItem.query.all()       
         product_items_schema=ProductItemSchema(many=True)
         return product_items_schema.jsonify(product_items), 200
     
       except Exception as e:
            return jsonify({'mes':"error "}),500
        
    def get_product_item(product_item_id):
        print(product_item_id)
        try:
            product_item=ProductItem.query.get(product_item_id)
            print(product_item)
            if not product_item :
                return {"errro":"Product item not found"},404
            product = Product.query.get(product_item.product_id)
            if not product:
                 return {"error": "Product details not found"}, 404
            wishlist_exists = False
            current_user = get_jwt_identity()
            if current_user:
                user_cart = ShoppingCart.query.filter_by(user_id=current_user['user_id']).first()
            if user_cart:
                wishlist_exists = WishlistItem.query.filter_by(
                    cart_id=user_cart.id, product_item_id=product_item.id).first() is not None

            result = {
                "id": product_item.id,
                "SKU": product_item.SKU,
                "qty_in_stock": product_item.qty_in_stock,
                "product_image": product_item.product_image,
                "price": product_item.price,
                "wishlist": wishlist_exists,
                "product": {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description
                }
            }
            return jsonify({"product_item": result}), 200
        except Exception as e:
            return jsonify({'mes': "error "}), 500


class ProductItemsByProductResource(Resource):
    def get(product_id):
        product = Product.query.get(product_id)
        if not product:
            return {"error": f"Product with id {product_id} does not exist"}, 404

        product_items = ProductItem.query.filter_by(product_id=product_id).all()

        product_items_schema=ProductItemSchema(many=True)
        return {
            "product_id": product_id,
            "product_name": product.name,
            "product_items": product_items_schema.dump(product_items)
        }, 200
    
    def get_product_items_by_category(category_id, selected_categories=None,):
        if selected_categories is None:
             selected_categories = []
        # data = request.get_json()
        # category_id = data.get("category_id")
       
        subcategories = []
        if not category_id:
            subcategories = [
                cat.id for cat in ProductCategory.query.all()
            ]
        #   return jsonify({"error": "category_id is required"}), 400
        else :
            subcategories = [category_id]
            if selected_categories:
              subcategories = [
              cat.id for cat in ProductCategory.query.filter(ProductCategory.category_name.in_(selected_categories)).all()
                ]
            else:
              queue = [category_id] 

              while queue:
                 current_category = queue.pop(0)
                 sub_cats = ProductCategory.query.filter_by(parent_category_id=current_category).all()
                 for sub_cat in sub_cats:
                     subcategories.append(sub_cat.id)
                     queue.append(sub_cat.id)  
        # print(subcategories)
        products = Product.query.filter(Product.category_id.in_(subcategories)).all()
        product_ids = [product.id for product in products]

        if not product_ids:
          return jsonify({"message": "No products found for this category"}), 404

        product_items = db.session.query(
             ProductItem.id,
             ProductItem.SKU,
             ProductItem.qty_in_stock,
             ProductItem.product_image,
             ProductItem.price,
             ProductItem.product_id,
             Product.name.label("product_name"),
             Product.description.label("product_description")
          ).join(Product, ProductItem.product_id == Product.id).filter(ProductItem.product_id.in_(product_ids)).all()

        if not product_items:
             return jsonify({"message": "No product items found for these products"}), 404
        
        wishlist_items = set()
        current_user = get_jwt_identity()
        # print(current_user)
        if current_user:
            user_cart = ShoppingCart.query.filter_by( user_id=current_user['user_id']).first()
            wishlist_items = {
                w.product_item_id for w in WishlistItem.query.filter_by(cart_id=user_cart.id).all()}

        result = [
            {
            "id": item.id,
            "SKU": item.SKU,
            "qty_in_stock": item.qty_in_stock,
            "product_image": item.product_image,
            "price": item.price,
            "wishlist": item.id in wishlist_items if current_user else False,
            "product": {
                "id": item.product_id,
                "name": item.product_name,
                "description": item.product_description
                 }
            }
            for item in product_items
        ]

        return jsonify({"product_items": result}), 200

class ProductItemDetailResource(Resource):
    def put(item_id):
        data = request.form
        print(data)
        product_item = ProductItem.query.get(item_id)
        if not product_item:
            return {"error": f"Product item with id {item_id} does not exist"}, 404
        if not data.get('SKU'):
            return{"error":'SKU required'},400
        if not data.get('qty_in_stock'):
            return {"error":'qty_in_stock required'},400
        if not data.get('price'):
            return {"error":'price required'},400
        if not data.get('product_id'):
            return{"error":'product_id required'},400
    
        product_item.SKU = data.get('SKU')
        product_item.product_id=data.get('product_id')
        product_item.qty_in_stock = data.get('qty_in_stock')
        product_item.price = data.get('price')
        if "product_image" in request.files:
                print("D")
                file = request.files["product_image"]
                if file.filename == "":
                    return {"error": "No selected file"}, 400
                if not isAllowedFile(file):
                    return {"error": "Invalid image format. Allowed formats: PNG, JPG, JPEG, GIF, BMP, WEBP"}, 400
                product_item.product_image = uploadfile(file,file.filename)

        db.session.commit()

        return {
            "message": "Product item updated successfully"
        }, 200

    def delete(item_id):
        try:
            product_item = ProductItem.query.get(item_id)
            if not product_item:
                return {"error": f"Product item with id {item_id} does not exist"}, 404

            db.session.delete(product_item)
            db.session.commit()

            return {"message": f"Product item with id {item_id} deleted successfully"}, 200
        except Exception as e:
             return jsonify({'mes':"error "}),500

