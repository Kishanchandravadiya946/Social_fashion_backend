from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models.product_item import ProductItem
from models.product import Product
from models.product_category import ProductCategory
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
        product_image = None
        price = data.get('price')
        print(product_id,SKU,qty_in_stock,price)
        if not product_id or not SKU or qty_in_stock is None or price is None:
            return {"error": "product_id, SKU, qty_in_stock, and price are required"}, 400

        product = Product.query.get(product_id)
        if not product:
            return {"error": f"Product with id {product_id} does not exist"}, 404

        if "product_image" in request.files:
            file = request.files["product_image"]
            if file.filename == "":
                return {"error": "No selected file"}, 400
            if not isAllowedFile(file):
                return {"error": "Invalid image format. Allowed formats: PNG, JPG, JPEG, GIF, BMP, WEBP"}, 400
            product_image = uploadfile(file,file.filename)
        
        
        new_product_item = ProductItem(
            product_id=product_id,
            SKU=SKU,
            qty_in_stock=qty_in_stock,
            product_image=product_image,
            price=price
        )
        
        db.session.add(new_product_item)
        db.session.commit()
        
        product_item_schema=ProductItemSchema()
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
    
    def get_product_items_by_category():
    
        data = request.get_json()
        category_id = data.get("category_id")

        if not category_id:
          return jsonify({"error": "category_id is required"}), 400

        subcategories = [category_id]  # Include the main category
        queue = [category_id]  # To process subcategories

        while queue:
         current_category = queue.pop(0)
         sub_cats = ProductCategory.query.filter_by(parent_category_id=current_category).all()
         for sub_cat in sub_cats:
            subcategories.append(sub_cat.id)
            queue.append(sub_cat.id)  

        products = Product.query.filter(Product.category_id.in_(subcategories)).all()
        product_ids = [product.id for product in products]

        if not product_ids:
          return jsonify({"message": "No products found for this category"}), 404

        product_items = ProductItem.query.filter(ProductItem.product_id.in_(product_ids)).all()

        if not product_items:
          return jsonify({"message": "No product items found for these products"}), 404

        product_item_schema = ProductItemSchema(many=True)
        return jsonify({"product_items": product_item_schema.dump(product_items)}), 200


class ProductItemDetailResource(Resource):
    def put(item_id):
        data = request.get_json()

        product_item = ProductItem.query.get(item_id)
        if not product_item:
            return {"error": f"Product item with id {item_id} does not exist"}, 404

        product_item.SKU = data.get('SKU', product_item.SKU)
        product_item.qty_in_stock = data.get('qty_in_stock', product_item.qty_in_stock)
        product_item.product_image = data.get('product_image', product_item.product_image)
        product_item.price = data.get('price', product_item.price)

        db.session.commit()

        product_item_schema=ProductItemSchema()
        return {
            "message": "Product item updated successfully",
            "product_item": product_item_schema.dump(product_item)
        }, 200

    def delete( item_id):
        product_item = ProductItem.query.get(item_id)
        if not product_item:
            return {"error": f"Product item with id {item_id} does not exist"}, 404

        db.session.delete(product_item)
        db.session.commit()

        return {"message": f"Product item with id {item_id} deleted successfully"}, 200
