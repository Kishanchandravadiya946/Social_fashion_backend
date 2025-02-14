from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models.variation_option import VariationOption
from models.variation import Variation
from ..schemas.variation_option_schema import VartationOptionSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

class VariationOptionResource(Resource):
    def post():
        current_user = get_jwt_identity()
        if current_user['role'] != 'admin':
               return jsonify({'error': 'Unauthorized access'}), 403 
        data = request.get_json()

        variation_id = data.get('variation_id')
        value = data.get('value')

        if not variation_id or not value:
            return {"error": "variation_id and value are required"}, 400

        variation = Variation.query.get(variation_id)
        if not variation:
            return {"error": f"Variation with id {variation_id} does not exist"}, 404

        new_option = VariationOption(
            variation_id=variation_id,
            value=value
        )

        db.session.add(new_option)
        db.session.commit()

        variation_option_schema=VartationOptionSchema()
        return {
            "message": "Variation option created successfully",
            "variation_option": variation_option_schema.dump(new_option)
        }, 201


class VariationOptionsByVariationResource(Resource):
    def get(variation_id):
        variation = Variation.query.get(variation_id)
        if not variation:
            return {"error": f"Variation with id {variation_id} does not exist"}, 404

        options = VariationOption.query.filter_by(variation_id=variation_id).all()

        variation_options_schema=VartationOptionSchema(many=True)
        return {
            "variation_id": variation_id,
            "variation_name": variation.name,
            "options": variation_options_schema.dump(options)
        }, 200
