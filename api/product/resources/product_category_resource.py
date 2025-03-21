from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models.product_category import ProductCategory
from ..schemas.product_category_schema import ProductCategorySchema
from flask_jwt_extended import jwt_required, get_jwt_identity

class ProductCategoryResource(Resource):
    def create_category():
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
               return jsonify({'error': 'Unauthorized access'}), 403 
        data = request.get_json()
        # print(data)
        category_name = data.get('category_name')
        parent_category_id = data.get('parent_category_id', None)  #here we get name
        existing_category = ProductCategory.query.filter_by(category_name=parent_category_id).first()
        # print(existing_category)
        if existing_category:
            parent_category_id =existing_category.id      
            # print(existing_category)
        
        if not category_name:
            # print("A")
            return {"error": "category_name is required"}, 400

        existing_category = ProductCategory.query.filter_by(category_name=category_name,parent_category_id=parent_category_id).first()
        if existing_category:
            # print("B")
            return {"error": "Category with this name already exists"}, 400
    
        if parent_category_id:
            parent_category = ProductCategory.query.get(parent_category_id)
            if not parent_category:
                # print("C",parent_category_id)
                return {"error": "Parent category does not exist"}, 400
        
        new_category = ProductCategory(
            category_name=category_name,
            parent_category_id=parent_category_id
        )

        try:
            db.session.add(new_category)
            db.session.commit()
            # print("D")
            return jsonify({'message': 'Product Cateogory created successfully!', '_id': new_category.id}), 201
            # return jsonify({'mass':"ok"})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

       

    def list_categories():
        try:
         categories = ProductCategory.query.all()
         productcetogories=ProductCategorySchema(many=True)
        #  print(productcetogories.jsonify(categories))
         return productcetogories.dump(categories), 200
        except Exception as e:
            return jsonify({'mes':"error "}),500
        
    def update_category(category_id):
        try:
            if not category_id:
                return jsonify({'error':"category id required"}),400
            categories=ProductCategory.query.get(category_id)
            if not categories:
                return jsonify({'error':"category not found"}),400
            data = request.get_json()

            categories.category_name=data.get('category_name') 

            if not data.get('category_name'):
                return jsonify({'error':"category name can't be empty"}),400
            # print(data.get('parent_category_id'))
            if data.get('parent_category_id'):
                parent_category=ProductCategory.query.get(data.get('parent_category_id'))
                if not parent_category :
                  return jsonify({'error':"category not found"}),400
                categories.parent_category_id=parent_category.id
            else:
                categories.parent_category_id = None
            db.session.commit()
            return {
            "message": "Product category updated successfully",
             }, 200
        except Exception as e:
            return jsonify({}),200
        
    
    def get_category(category_id):
        try:
            category = ProductCategory.query.get(category_id)
            productcetogories=ProductCategorySchema()

            if not category:
                return jsonify({'message': 'Category not found'}), 404
            return jsonify(productcetogories.dump(category)), 200
        except Exception as e:
            return jsonify({'message': "Error retrieving category"}), 500
    
    def delete_category(category_id):
        try:
            if not category_id:
                return {"error":"product required"},400
            category = ProductCategory.query.get(category_id)
            if not category:
                return {"error":"catwgory with category id : {category_id} doesn't exist"},400
            
         
            db.session.delete(category)
            db.session.commit()
            return jsonify({"message": f"Category with category id: {category_id} deleted successfully"}), 200
        except Exception as e:
            return jsonify({"message":'Error deleting category'}),500
