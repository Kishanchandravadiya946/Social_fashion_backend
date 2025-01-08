from app import db

class ShoppingCartItem(db.Model):
    __tablename__ = 'shopping_cart_item'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('shopping_cart.id'), nullable=False)
    product_item_id = db.Column(db.Integer, db.ForeignKey('product_item.id'), nullable=False)
    qty = db.Column(db.Integer, nullable=False)