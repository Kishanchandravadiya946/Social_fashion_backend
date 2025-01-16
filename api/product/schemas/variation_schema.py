from extensions import ma
from models.variation import Variation

class VariationSchema(ma.SQLAlchemyAutoSchema):
    class meta:
        model = Variation
        load_instance=True
        
    