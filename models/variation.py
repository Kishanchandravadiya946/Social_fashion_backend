from extensions import db

class Variation(db.Model):
    __tablename__ = 'variation'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)