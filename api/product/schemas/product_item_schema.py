from extensions import ma
from models.product_item import ProductItem

class ProductItemSchema(ma.SQLAlchemyAutoSchema) :
    class Meta:
        model = ProductItem
        load_instance = True
        include_fk=True