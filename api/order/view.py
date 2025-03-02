from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from .resources.order_resource import ShippingMethodResource
shop_order=Blueprint('shop_order',__name__,url_prefix="/order");

@shop_order.route('/shipping_method/list',methods=['GET'])
@jwt_required()
def shipping_method_schema():
    return ShippingMethodResource.shipping_method_list()


@shop_order.route('/create-payment-intent', methods=['POST'])
@jwt_required()
def payment_intent():
    return ShippingMethodResource.create_payment_intent()


@shop_order.route('/checkout/place_order',methods=['POST'])
@jwt_required()
def place_order():
    return ShippingMethodResource.place_order()

@shop_order.route('/shop',methods=['GET'])
@jwt_required()
def shop_order_list():
    return ShippingMethodResource.get_user_orders()