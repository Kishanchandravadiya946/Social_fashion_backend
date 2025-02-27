from extensions import ma
from models.variation import Variation

class VariationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Variation
        load_instance= True
        include_fk=True
        
    