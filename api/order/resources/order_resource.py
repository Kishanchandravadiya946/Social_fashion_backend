from flask import request, jsonify
from flask_restful import Resource
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.shipping_method import ShippingMethod
from models.product import Product
from models.order_line import OrderLine
from models.shop_order import ShopOrder
from models.user_payment_method import UserPaymentMethod
from models.shopping_cart_item import ShoppingCartItem
from models.shopping_cart import ShoppingCart
from models.order_status import OrderStatus
from models.product_item import ProductItem
from models.site_user import SiteUser
from ..schemas.shipping_method_schema import ShippingMethodSchema
import stripe
from config import Config
from datetime import datetime, timedelta
import random

stripe.api_key = Config.STRIPE_SECRET_KEY


class ShippingMethodResource(Resource):
    def shipping_method_list():
        try:
            shipping_method_list = ShippingMethod.query.all()
            schema = ShippingMethodSchema(many=True)
            return schema.dump(shipping_method_list), 200
        except Exception as e:
            return jsonify({'mes': "error "}), 500

    def create_payment_intent():
        try:
            data = request.get_json()
            amount = data.get("amount")
            if not amount or amount <= 0:
                return jsonify({"error": "Invalid amount"}), 400

            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency="usd",
                payment_method_types=["card"]
            )

            return jsonify({"clientSecret": payment_intent["client_secret"]}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def place_order():
        try:
            data = request.get_json()
            if not data:
                return jsonify({"message": "Invalid JSON data"}), 400

            current_user = get_jwt_identity()
            if not current_user or 'user_id' not in current_user:
                return jsonify({'message': 'Unauthorized access'}), 401

            random_years = random.randint(1, 5)
            # print(data)
            new_payment = UserPaymentMethod(
                user_id=current_user['user_id'],
                payment_type_id=1,
                provider="Stripe",
                account_number="4242 4242 4242 4242",
                expiry_date=datetime.now() + timedelta(days=random_years * 365),
            )

            db.session.add(new_payment)
            db.session.commit()
            # print(new_payment)
            # Create Shop Order
            new_order = ShopOrder(
                user_id=current_user['user_id'],
                order_date=datetime.now(),
                payment_method_id=new_payment.id,
                shipping_address=data.get("shipping_address"),
                shipping_method=data.get("shipping_method"),
                order_total=data.get("order_total"),
                order_status=1
            )
            db.session.add(new_order)
            db.session.commit()
            # print(new_order)
            order_lines = []
            for item in data.get("items", []):
                order_line = OrderLine(
                    product_item_id=item["product_item_id"],
                    order_id=new_order.id,
                    qty=item["qty"],
                    price=item["price"]
                )
                order_lines.append(order_line)

            db.session.add_all(order_lines)
            db.session.commit()
            # print(order_lines)
            user_cart = ShoppingCart.query.filter_by(
                user_id=current_user['user_id']).first()
            if user_cart:
                ShoppingCartItem.query.filter_by(cart_id=user_cart.id).delete()
                db.session.commit()

            return jsonify({"message": "Order placed successfully!"}), 201

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500
        
    def get_user_orders():
      try:
        current_user = get_jwt_identity()
        if not current_user or 'user_id' not in current_user:
            return jsonify({'message': 'Unauthorized access'}), 401

        user_id = current_user['user_id']

        orders = ShopOrder.query.filter_by(user_id=user_id).all()
        if not orders:
            return jsonify({"message": "No orders found"}), 404

        order_list = []
        for order in orders:
            order_status = OrderStatus.query.filter_by(
                id=order.order_status).first()

            order_lines = OrderLine.query.filter_by(order_id=order.id).all()
            items = []
            for line in order_lines:
                product = ProductItem.query.filter_by(
                    id=line.product_item_id).first()
                productName = Product.query.filter_by(id=product.product_id).first() if product else None
                product_name = productName.name if productName else "Unknown"
                items.append({
                    "product_id": product.id,
                    "product_image": product.product_image,
                    "qty": line.qty,
                    "price": line.price,
                    "product_name":product_name
                })

            order_list.append({
                "order_id": order.id,
                "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
                "order_status": order_status.status if order_status else "Unknown",
                "shipping_address": order.shipping_address,
                "shipping_method": order.shipping_method,
                "order_total": order.order_total,
                "items": items
            })

        return jsonify(order_list), 200

      except Exception as e:
        return jsonify({"error": str(e)}), 500

    def get_all_orders():
        try:
            current_user = get_jwt_identity()
            if not current_user or 'role' not in current_user or current_user['role'] != 'admin':
                return jsonify({'message': 'Unauthorized access'}), 401

            orders = ShopOrder.query.all()  # Fetch all orders
            
            if not orders:
                return jsonify({"message": "No orders found"}), 404

            order_list = []
            for order in orders:
                order_status = OrderStatus.query.filter_by(id=order.order_status).first()

                user = SiteUser.query.filter_by(id=order.user_id).first()
                username = user.username if user else "Unknown"

                order_lines = OrderLine.query.filter_by(order_id=order.id).all()
                items = []
                for line in order_lines:
                    product_item = ProductItem.query.filter_by(id=line.product_item_id).first()
                    product = Product.query.filter_by(id=product_item.product_id).first() if product_item else None
                    product_name = product.name if product else "Unknown"
                    items.append({
                        "product_id": product_name,
                        "product_image": product_item.product_image if product_item else None,
                        "qty": line.qty,
                        "price": line.price
                    })

                order_list.append({
                    "order_id": order.id,
                    "username": username,  # Include user ID to differentiate orders
                    "order_date": order.order_date.strftime("%Y-%m-%d %H:%M:%S"),
                    "order_status": order_status.status if order_status else "Unknown",
                    "order_status_id": order_status.id if order_status else "Unknown",
                    "shipping_address": order.shipping_address,
                    "shipping_method": order.shipping_method,
                    "order_total": order.order_total,
                    "items": items
                })

            return jsonify(order_list), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    def change_order_status():
        try:
            data = request.get_json()
            order_id = data.get("order_id")
            new_status_id = data.get("status_id")  
            # print(order_id,new_status_id)
            order = ShopOrder.query.get(order_id)
            status = OrderStatus.query.get(new_status_id)
            # print(status ,order)
            if not order:
                return jsonify({"message": "Order not found"}), 404
            if not status:
                return jsonify({"message": "Invalid status ID"}), 400

            order.order_status = status.id
            db.session.commit()

            return jsonify({"message": "Order status updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "An error occurred", "error": str(e)}), 500
        

    def get_all_status():
        try:
            statuses = OrderStatus.query.all()
            status_list = [{"id": status.id, "name": status.status} for status in statuses]
            return jsonify(status_list), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
