from extensions import ma
from models.product_configuration import ProductConfiguration

class ProductConfigurationSchema(ma.SQLAlchemyAutoSchema) :
    class meta:
        model = ProductConfiguration
        load_instance =True 

