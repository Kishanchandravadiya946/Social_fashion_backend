from extensions import ma
from models.product_category import ProductCategory

class ProductCategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=ProductCategory
        load_instance = True