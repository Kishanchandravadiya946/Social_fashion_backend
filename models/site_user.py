from extensions import db

class SiteUser(db.Model):
    __tablename__ = 'site_user'
    id = db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(255),nullable=False)
    email_address = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=True)
    password = db.Column(db.String(255), nullable=False)
