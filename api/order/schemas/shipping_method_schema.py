from extensions import ma
from models.shipping_method import ShippingMethod

class ShippingMethodSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ShippingMethod
        load_instance = True