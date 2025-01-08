from app import db

class ProductItem(db.Model):
    __tablename__ = 'product_item'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    SKU = db.Column(db.String(50), nullable=False)
    qty_in_stock = db.Column(db.Integer, nullable=False)
    product_image = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)