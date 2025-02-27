from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from .resources.order_resource import ShippingMethodResource
shop_order=Blueprint('shop_order',__name__,url_prefix="/order");

@shop_order.route('/shipping_method/list',methods=['GET'])
@jwt_required()
def shipping_method_schema():
    return ShippingMethodResource.shipping_method_list()
