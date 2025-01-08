from app import db

class ProductCategory(db.Model):
    __tablename__ = 'product_category'
    id = db.Column(db.Integer, primary_key=True)
    parent_category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'))
    category_name = db.Column(db.String(100), nullable=False)