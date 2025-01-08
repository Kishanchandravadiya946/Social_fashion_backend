from app import db

class OrderLine(db.Model):
    __tablename__ = 'order_line'
    id = db.Column(db.Integer, primary_key=True)
    product_item_id = db.Column(db.Integer, db.ForeignKey('product_item.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('shop_order.id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)