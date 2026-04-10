import cloudinary
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from src.app.database.base import Base

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def init_cloudinary(app):
    cloudinary.config(
        cloud_name = app.config['CLOUDINARY_NAME'],
        api_key = app.config['CLOUDINARY_API_KEY'],
        api_secret = app.config['CLOUDINARY_API_SECRET'],
        secure = True
    )