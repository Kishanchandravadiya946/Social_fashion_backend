from app import db

class ShopOrder(db.Model):
    __tablename__ = 'shop_order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('site_user.id'), nullable=False)
    order_date = db.Column(db.DateTime, nullable=False)
    payment_method_id = db.Column(db.Integer, db.ForeignKey('user_payment_method.id'), nullable=False)
    shipping_address = db.Column(db.Integer, db.ForeignKey('address.id'), nullable=False)
    shipping_method = db.Column(db.Integer, db.ForeignKey('shipping_method.id'), nullable=False)
    order_total = db.Column(db.Float, nullable=False)
    order_status = db.Column(db.Integer, db.ForeignKey('order_status.id'), nullable=False)
