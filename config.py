import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

class Config:
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() == 'true'
    
    HOST=os.getenv("FLASK_RUN_HOST")
    PORT=os.getenv("FLASK_RUN_PORT")
    DEBUG_APP=os.getenv("FLASK_DEBUG")
    
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY",'default_secret_key')
    JWT_TOKEN_LOCATION=["headers"] 
    JWT_IDENTITY_CLAIM="user_id"
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=60)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]