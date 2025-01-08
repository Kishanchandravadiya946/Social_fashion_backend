from app import db

class WishlistItem(db.Model):
    __tablename__ = 'wishlist_item'
    id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('shopping_cart.id'), nullable=False)
    product_item_id = db.Column(db.Integer, db.ForeignKey('product_item.id'), nullable=False)
