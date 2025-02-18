from extensions import ma
from models.shopping_cart_item import ShoppingCartItem

class ShoppingCartItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=ShoppingCartItem
        load_instance=True