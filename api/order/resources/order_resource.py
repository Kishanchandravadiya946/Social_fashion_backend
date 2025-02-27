from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.shipping_method import ShippingMethod
from ..schemas.shipping_method_schema import ShippingMethodSchema


class ShippingMethodResource(Resource):
    def shipping_method_list():
        try:
            shipping_method_list = ShippingMethod.query.all()
            schema = ShippingMethodSchema(many=True)
            return schema.dump(shipping_method_list), 200
        except Exception as e:
            return jsonify({'mes': "error "}), 500
