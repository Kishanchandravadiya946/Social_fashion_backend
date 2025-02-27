from extensions import db


class OrderStatus(db.Model):
    __tablename__ = 'order_status'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)
