from flask import Flask
from config import Config
from extensions import db
from flask_migrate import Migrate
from models import init_models

app=Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
init_models(db)
migrate = Migrate(app,db)
   
with app.app_context():
        db.create_all() 

if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG_APP,
    )