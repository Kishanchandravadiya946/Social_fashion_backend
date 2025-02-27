from extensions import ma
from models.product_configuration import ProductConfiguration

class ProductConfigurationSchema(ma.SQLAlchemyAutoSchema) :
    class Meta:
        model = ProductConfiguration
        load_instance =True 

