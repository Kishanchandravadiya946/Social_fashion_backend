from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models.variation import Variation
from models.product_category import ProductCategory
from ..schemas.variation_schema import VariationSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

class VariationResource(Resource):
    def post():
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
               return jsonify({'error': 'Unauthorized access'}), 403 
        data = request.get_json()

        category_id = data.get('category_id')
        name = data.get('name')

        if not category_id or not name:
            return {"error": "category_id and name are required"}, 400

        category = ProductCategory.query.get(category_id)
        if not category:
            return {"error": f"Category with id {category_id} does not exist"}, 404

        new_variation = Variation(
            category_id=category_id,
            name=name
        )

        db.session.add(new_variation)
        db.session.commit()
        
        variation_schema=VariationSchema()
        return {
            "message": "Variation created successfully",
            "variation": variation_schema.dump(new_variation)
        }, 201
        
    def get():
        variations = Variation.query.all()
        variation_schema = VariationSchema(many=True)
        return  variation_schema.jsonify(variations)

class VariationsByCategoryResource(Resource):
    def get( category_id):
        category = ProductCategory.query.get(category_id)
        if not category:
            return {"error": f"Category with id {category_id} does not exist"}, 404

        variations = Variation.query.filter_by(category_id=category_id).all()
        
        variations_schema=VariationSchema(many=True)
        return {
            "category_id": category_id,
            "category_name": category.category_name,
            "variations": variations_schema.dump(variations)
        }, 200
