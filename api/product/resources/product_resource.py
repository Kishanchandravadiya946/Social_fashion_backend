from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models.product import Product
from models.product_category import ProductCategory
from ..schemas.product_schema import ProductSchema


class ProductResource(Resource):
    def create():
        data = request.get_json()

        category_id = data.get('category_id')
        name = data.get('name')
        description = data.get('description', '')
        product_image = data.get('product_image', '')

        if not category_id:
            return {"error": "category_id is required"}, 400

        if not name:
            return {"error": "name is required"}, 400

        category = ProductCategory.query.get(category_id)
        if not category:
            return {"error": f"Category with id {category_id} does not exist"}, 404

        new_product = Product(
            category_id=category_id,
            name=name,
            description=description,
            product_image=product_image
        )

        db.session.add(new_product)
        db.session.commit()
        
        product_schema=ProductSchema()
        return {
            "message": "Product created successfully",
            "product": product_schema.dump(new_product)
        }, 201

    def Product_list():
        products = Product.query.all()
        products_schema=ProductSchema(many=True)
        return {"products": products_schema.dump(products)}, 200


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
 

