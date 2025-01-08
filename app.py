from flask import Flask
from config import Config
from extensions import db
from flask_migrate import Migrate
from models import init_models
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app=Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    return app

def register_extensions(app):
    db.init_app(app)
    init_models(db)
    migrate = Migrate(app,db)
    

if __name__ == '__main__':
    app=create_app()
    # print("hiiiiiiiiiiiiiiiiiiiii")
    # print(os.getenv("FLASK_RUN_HOST"))
    app.run(
        host=os.getenv("FLASK_RUN_HOST"),
        port=os.getenv("FLASK_RUN_PORT"),
        debug=os.getenv("FLASK_DEBUG"),
    )
   
    with app.app_context():
        db.create_all()
    # app.run('127.0.0.1',5000)