from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from models.product import Product
from models.product_category import ProductCategory
from ..schemas.product_schema import ProductSchema


class ProductResource(Resource):
    # Method to create a product
    def create():
        data = request.get_json()

        # Extract and validate data
        category_id = data.get('category_id')
        name = data.get('name')
        description = data.get('description', '')
        product_image = data.get('product_image', '')

        if not category_id:
            return {"error": "category_id is required"}, 400

        if not name:
            return {"error": "name is required"}, 400

        # Check if the category exists
        category = ProductCategory.query.get(category_id)
        if not category:
            return {"error": f"Category with id {category_id} does not exist"}, 404

        # Create a new Product instance
        new_product = Product(
            category_id=category_id,
            name=name,
            description=description,
            product_image=product_image
        )

        # Save to the database
        db.session.add(new_product)
        db.session.commit()
        product_schema=ProductSchema()
        # Serialize and return the created product
        return {
            "message": "Product created successfully",
            "product": product_schema.dump(new_product)
        }, 201

    # Method to get all products
    def Product_list():
        # Fetch all products
        products = Product.query.all()
        products_schema=ProductSchema(many=True)
        # Serialize and return products
        return {"products": products_schema.dump(products)}, 200


class CategoryWiseProductResource(Resource):
    # Method to get products by category
    def get(category_id):
        # Check if the category exists
        category = ProductCategory.query.get(category_id)
        if not category:
            return {"error": f"Category with id {category_id} does not exist"}, 404

        # Fetch products for the given category
        products = Product.query.filter_by(category_id=category_id).all()

        products_schema=ProductSchema(many=True)
        # Serialize and return products
        return {
            "category_id": category_id,
            "category_name": category.category_name,
            "products": products_schema.dump(products)
        }, 200
 

