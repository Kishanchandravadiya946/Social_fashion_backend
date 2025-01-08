from app import db

class ShippingMethod(db.Model):
    __tablename__ = 'shipping_method'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)