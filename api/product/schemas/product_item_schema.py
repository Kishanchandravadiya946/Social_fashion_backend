from extensions import ma
from models.product_item import ProductItem

class ProductItemSchema(ma.SQLAlchemyAutoSchema) :
    class Meta:
        model : ProductItem
        load_instance = True
        fields = ("SKU", "qty_in_stock", "product_image", "price")

    product = ma.Nested('ProductSchema', many=False)