from flask import Blueprint,request
from .resources.product_category_resource import ProductCategoryResource
from .resources.product_resource import ProductResource,CategoryWiseProductResource
from .resources.product_item_resource import ProductItemResource,ProductItemDetailResource,ProductItemsByProductResource
from .resources.variation_resource import VariationResource,VariationsByCategoryResource
from .resources.variation_option_resource import VariationOptionResource,VariationOptionsByVariationResource
from flask_jwt_extended import jwt_required, get_jwt_identity

product_category_bp= Blueprint('product_catogory', __name__ , url_prefix='/product_category')

@product_category_bp.route('/create',methods=['POST'])
@jwt_required()
def create_product_catogory():
    return ProductCategoryResource.create_category()
@product_category_bp.route('/list',methods=['GET'])
def get_product_categories():
    return ProductCategoryResource.list_categories()
@product_category_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    return ProductCategoryResource.get_category(category_id)
@product_category_bp.route('/update/<int:category_id>',methods=['PUT'])
def update_product_categories(category_id):
    return ProductCategoryResource.update_category(category_id)
@product_category_bp.route('/delete/<int:category_id>',methods=['DELETE'])
def delete_product_category(category_id):
    return ProductCategoryResource.delete_category(category_id)



product_bp= Blueprint('Product', __name__ , url_prefix = '/product')
@product_bp.route('/create',methods=['POST'])
@jwt_required()
def create_product():
    return ProductResource.create()

@product_bp.route('/list',methods=['GET'])
def list_product():
    return ProductResource.Product_list()

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    return ProductResource.get_product(product_id)
@product_bp.route('/update/<int:product_id>',methods=['PUT'])
def update_product(product_id):
    return ProductResource.product_update(product_id)
@product_bp.route('/delete/<int:product_id>',methods=['DELETE'])
def delete_product(product_id):
    return ProductResource.product_delete(product_id)

@product_bp.route('/<int:category_id>/products',methods=['GET'])
def category_wise_product(category_id):
    return CategoryWiseProductResource.get(category_id) 
@product_bp.route('/products/category/<int:category_id>', methods=['GET'])
def get_products_by_category(category_id):
    return ProductResource.get_products_by_top_category(category_id)



product_item_bp= Blueprint('ProductItem', __name__ , url_prefix ='/product_item')
@product_item_bp.route('/create',methods=['POST'])
@jwt_required()
def create_product_item():
    return ProductItemResource.post()

@product_item_bp.route('/list',methods=['GET'])
def list_product_item():
    return ProductItemResource.get()

@product_item_bp.route('/<int:product_item_id>',methods=['GET'])
@jwt_required()
def product_item(product_item_id):
    return ProductItemResource.get_product_item(product_item_id)
@product_item_bp.route('/product/<int:product_id>',methods=['GET'])
def product_product_item_list():
    return ProductItemsByProductResource.get()

@product_item_bp.route('/category/<int:category_id>',methods=['GET'])
@jwt_required(optional=True)
def product_item_category(category_id):
    filters = request.args.get("f") 
    selected_categories = filters.split(",") if filters else []
    return ProductItemsByProductResource.get_product_items_by_category(category_id, selected_categories)

@product_item_bp.route('update/<int:item_id>',methods=['PUT'])
def update_product_item(item_id):
    return ProductItemDetailResource.put(item_id)

@product_item_bp.route('delete/<int:item_id>',methods=['DELETE'])
def delete_product_item(item_id):
    return ProductItemDetailResource.delete(item_id)



variation_bp= Blueprint("Variation",__name__ ,url_prefix='/variation')
@variation_bp.route('/create',methods=['POST'])
@jwt_required()
def create_variation():
    return VariationResource.post()
@variation_bp.route('/list',methods=['GET'])
def list_variation():
    return VariationResource.get()

@variation_bp.route('/<int:category_id>',methods=['GET'])
def categories_variation():
    return VariationsByCategoryResource.get()



variation_option_bp=Blueprint("Variation_option",__name__ , url_prefix='/variation_option')
@variation_option_bp.route('/create',methods=['POST'])
@jwt_required()
def create_variation_optoion():
    return VariationOptionResource.post()
@variation_option_bp.route('/list',methods=['GET'])
def variation_option_list():
    return VariationOptionResource.get()

@variation_option_bp.route('/<int:variation_id>',methods=['GET'])
def variation_variation_option_list():
    return VariationOptionsByVariationResource.get()