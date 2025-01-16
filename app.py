from flask import Flask
from config import Config
from extensions import db
from flask_migrate import Migrate
from models import init_models
from api.user.views import user_bp
from api.product.views import product_category_bp,product_bp,product_item_bp,variation_bp,variation_option_bp


app=Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
init_models(db)
migrate = Migrate(app,db)
   
app.register_blueprint(user_bp)
app.register_blueprint(product_category_bp)
app.register_blueprint(product_bp)
app.register_blueprint(product_item_bp)
app.register_blueprint(variation_bp)
app.register_blueprint(variation_option_bp)

with app.app_context():
        db.create_all() 

if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG_APP,
    )