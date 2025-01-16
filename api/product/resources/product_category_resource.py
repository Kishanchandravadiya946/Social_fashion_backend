from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models.product_category import ProductCategory
from ..schemas.product_category_schema import ProductCategorySchema

class ProductCategoryResource(Resource):
    # Method to create a category
    def create_category():
        data = request.get_json()
        category_name = data.get('category_name')
        parent_category_id = data.get('parent_category_id', None)

        if not category_name:
            return {"error": "category_name is required"}, 400

        # Create a new ProductCategory instance
        new_category = ProductCategory(
            category_name=category_name,
            parent_category_id=parent_category_id
        )

        # Add to the database
        try:
            db.session.add(new_category)
            db.session.commit()
            return jsonify({'message': 'Product Cateogory created successfully!', '_id': new_category.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

       

    # Method to list all categories
    def list_categories():
        # Fetch all categories
        try:
         categories = ProductCategory.query.all()
         productcetogories=ProductCategorySchema(many=True)
         return productcetogories.jsonify(categories), 200
        except Exception as e:
            return jsonify({'mes':"error "}),500
    
    
