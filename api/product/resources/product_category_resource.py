from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models.product_category import ProductCategory
from ..schemas.product_category_schema import ProductCategorySchema

class ProductCategoryResource(Resource):
    def create_category():
        data = request.get_json()
        category_name = data.get('category_name')
        parent_category_id = data.get('parent_category_id', None)

        if not category_name:
            return {"error": "category_name is required"}, 400

        new_category = ProductCategory(
            category_name=category_name,
            parent_category_id=parent_category_id
        )

        try:
            db.session.add(new_category)
            db.session.commit()
            return jsonify({'message': 'Product Cateogory created successfully!', '_id': new_category.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

       

    def list_categories():
        try:
         categories = ProductCategory.query.all()
         productcetogories=ProductCategorySchema(many=True)
         return productcetogories.jsonify(categories), 200
        except Exception as e:
            return jsonify({'mes':"error "}),500
    
    
