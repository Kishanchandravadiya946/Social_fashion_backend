from app import db

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    product_image = db.Column(db.String(255))