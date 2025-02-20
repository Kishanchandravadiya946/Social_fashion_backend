from extensions import ma
from models.wishlist_item import WishlistItem

class WishListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=WishlistItem
        load_instance=True