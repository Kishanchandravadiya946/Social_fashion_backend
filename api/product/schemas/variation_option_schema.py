from extensions import ma
from models.variation_option import VariationOption

class VartationOptionSchema(ma.SQLAlchemyAutoSchema):
    class Meta :
        model =VariationOption
        load_instance =True
        include_fk=True