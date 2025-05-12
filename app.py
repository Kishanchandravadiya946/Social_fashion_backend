from flask import Flask
from config import Config
from extensions import db
from flask_migrate import Migrate
from models import init_models
from api.user.views import user_bp
from api.product.views import product_category_bp, product_bp, product_item_bp, variation_bp, variation_option_bp
from api.shopping_cart.view import shopping_cart_item, wishlist_bp
from api.order.view import shop_order
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from api.user.resources.user_resource import revoked_tokens
app = Flask(__name__)

app.config.from_object(Config)
print("HELLOOOOOO ")
CORS(app,
     origins=["https://mango-glacier-0805ada00.6.azurestaticapps.net/",
              "http://localhost:5173"],
     supports_credentials=True,
     resources={r"/*": {"origins": [
         "https://mango-glacier-0805ada00.6.azurestaticapps.net/",
         "http://localhost:5173"
     ]}},
     methods=["GET", "POST", "OPTIONS", "PUT", "DELETE"],
     allow_headers=["Content-Type", "Authorization"])

jwt = JWTManager(app)


@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload):
    #  print("a",revoked_tokens)
    jti = jwt_payload["jti"]
    return jti in revoked_tokens


db.init_app(app)
init_models(db)
migrate = Migrate(app, db)

app.register_blueprint(user_bp)
app.register_blueprint(product_category_bp)
app.register_blueprint(product_bp)
app.register_blueprint(product_item_bp)
app.register_blueprint(variation_bp)
app.register_blueprint(variation_option_bp)
app.register_blueprint(shopping_cart_item)
app.register_blueprint(wishlist_bp)
app.register_blueprint(shop_order)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG_APP,
    )
