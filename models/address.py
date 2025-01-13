from extensions import db

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    unit_number = db.Column(db.String(50))
    street_number = db.Column(db.String(50))
    address_line1 = db.Column(db.String(255))
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    region = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))
