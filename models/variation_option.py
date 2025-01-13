from extensions import db

class VariationOption(db.Model):
    __tablename__ = 'variation_option'
    id = db.Column(db.Integer, primary_key=True)
    variation_id = db.Column(db.Integer, db.ForeignKey('variation.id'), nullable=False)
    value = db.Column(db.String(100), nullable=False)