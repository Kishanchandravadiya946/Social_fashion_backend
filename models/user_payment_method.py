from app import db

class UserPaymentMethod(db.Model):
    __tablename__ = 'user_payment_method'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('site_user.id'), nullable=False)
    payment_type_id = db.Column(db.Integer, db.ForeignKey('payment_type.id'), nullable=False)
    provider = db.Column(db.String(255))
    account_number = db.Column(db.String(50))
    expiry_date = db.Column(db.Date)
    is_default = db.Column(db.Boolean, default=False)