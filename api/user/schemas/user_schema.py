from extensions import ma
from models.site_user import SiteUser

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SiteUser
        load_instance = True