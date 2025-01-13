from extensions import db

class ProductConfiguration(db.Model):
    __tablename__ = 'product_configuration'
    product_item_id = db.Column(db.Integer, db.ForeignKey('product_item.id'), primary_key=True)
    variation_option_id = db.Column(db.Integer, db.ForeignKey('variation_option.id'), primary_key=True)
