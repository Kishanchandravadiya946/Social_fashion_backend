from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models.product import Product
from models.product_category import ProductCategory
from models.product_item import ProductItem
from ..schemas.product_schema import ProductSchema
from ...shared.uploadFile import uploadfile 
from ...shared.isAllowedFile import isAllowedFile
import imghdr
from flask_jwt_extended import jwt_required, get_jwt_identity

class ProductResource(Resource):
       
    def create():
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
               return jsonify({'error': 'Unauthorized access'}), 403 
        data = request.form
        # print(data)
        category_id = data.get('category_id')
        name = data.get('name')
        description = data.get('description', '')
        product_image =None
        # print(category_id,name,description)  
        if not category_id:
            print("A")
            return {"error": "category_id is required"}, 400

        if not name:
            print("B")
            return {"error": "name is required"}, 400

        category = ProductCategory.query.get(category_id)
        if not category:
            print("C")
            return {"error": f"Category with id {category_id} does not exist"}, 404
        
        if "product_image" in request.files:
            print("D")
            file = request.files["product_image"]
            if file.filename == "":
                return {"error": "No selected file"}, 400
            if not isAllowedFile(file):
                return {"error": "Invalid image format. Allowed formats: PNG, JPG, JPEG, GIF, BMP, WEBP"}, 400
            product_image = uploadfile(file,file.filename)

        new_product = Product(
            category_id=category_id[0],
            name=name,
            description=description,
            product_image=product_image
        )
        print(category_id,name,description,product_image)
        db.session.add(new_product)
        db.session.commit()
        
        product_schema=ProductSchema()
        return {
            "message": "Product created successfully",
            "product": product_schema.dump(new_product)
        }, 201

    def Product_list():
        products = Product.query.all()
        products_schema=ProductSchema()
        product_data=[]
        for product in products:
            product_item=ProductItem.query.filter_by(product_id=product.id).first()
            product_dict=products_schema.dump(product)
            if product_item:
                product_dict["product_item_id"]=product_item.id
            product_data.append(product_dict)
        return  jsonify(product_data), 200
    
    def get_product(product_id):
        print(product_id)
        try:
            product = Product.query.get(product_id)
            if not product:
                return jsonify({'message': 'Product not found'}), 404
            product_schema=ProductSchema()
            print("hy")
            return jsonify(product_schema.dump(product)), 200
        except Exception as e:
            return jsonify({'message': "Error retrieving product"}), 500

    def product_update(product_id):
        try:
            data=request.form
            # print(data)
            product = Product.query.get(product_id)

            if not data.get('category_id'):
                # print("A")
                return {"error": "category_id is required"}, 400

            if not  data.get('name'):
                # print("B")
                return {"error": "name is required"}, 400

            if not  data.get('description'):
                # print("B")
                return {"error": "description is required"}, 400

            if not product:
                print("C")
                return {"error": f"product with id {product_id} does not exist"}, 404
        
            product.category_id = data.get('category_id')
            product.name = data.get('name')
            product.description = data.get('description', '')
            # product.product_image =None
            # print(category_id,name,description)  
            
            
            if "product_image" in request.files:
                print("D")
                file = request.files["product_image"]
                if file.filename == "":
                    return {"error": "No selected file"}, 400
                if not isAllowedFile(file):
                    return {"error": "Invalid image format. Allowed formats: PNG, JPG, JPEG, GIF, BMP, WEBP"}, 400
                product.product_image = uploadfile(file,file.filename)

            db.session.commit()
            return {
            "message": "Product updated successfully",
             }, 200

        except Exception as e:
            return jsonify({'message': "Error while updating product"}), 500
        
    def product_delete(product_id):
        try:
            if not product_id:
                return {"error":"product required"},400
            product = Product.query.get(product_id)
            if not product:
                return {"error":"product with id {product_id} doesn't exist"},400

            db.session.delete(product)
            db.session.commit()
            return jsonify({"message": f"product with id: {product_id} deleted successfully"}), 200


        except Exception as e:
            return jsonify({'message': "Error while updating product"}), 500
        

class CategoryWiseProductResource(Resource):
    def get(category_id):
        category = ProductCategory.query.get(category_id)
        if not category:
            return {"error": f"Category with id {category_id} does not exist"}, 404

        products = Product.query.filter_by(category_id=category_id).all()

        products_schema=ProductSchema(many=True)
        return {
            "category_id": category_id,
            "category_name": category.category_name,
            "products": products_schema.dump(products)
        }, 200
      
        
    def get_products_by_top_category(category_id):
        try:
            category_ids = {category_id}
            subcategories = ProductCategory.query.filter_by(parent_category_id=category_id).all()
            category_ids.update(subcategories)            
            products = Product.query.filter(Product.category_id.in_(category_ids)).all()

            if not products:
                return jsonify({'message': 'No products found for this category'}), 404
            products_schema=ProductSchema(many=True)
            return jsonify(products_schema.dump(products)), 200
        except Exception as e:
            return jsonify({'message': 'Error retrieving products'}), 500

 

