from app import db

class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(100), nullable=False)