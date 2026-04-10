import os
from dotenv import load_dotenv

load_dotenv()

class DevelopmentConfig():
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SECRET_KEY = os.getenv('SECRET_KEY', 'development_secret_key')
    AUTO_CREATE_TABLES = True
    SQL_ECHO = True
    DEBUG = True

    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')


class ProdcutionConfig():
    SQLALCHEMY_DATABASE_URIL = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ['SECRET_KEY']
    AUTO_CREATE_TABLES = False
    SQL_ECHO = False
    DEBUG = False

    CLOUDINARY_CLOUD_NAME = os.environ['CLOUDINARY_CLOUD_NAME']
    CLOUDINARY_API_KEY = os.environ['CLOUDINARY_API_KEY']
    CLOUDINARY_API_SECRET = os.environ['CLOUDINARY_API_SECRET']


APP_ENV = os.getenv('APP_ENV')
if not APP_ENV:
    raise RuntimeError('No se definio el valor de APP_ENV')

config_map = {
    "development":DevelopmentConfig,
    "production":ProdcutionConfig
}

configClass = config_map.get(APP_ENV)

if not configClass:
    raise RuntimeError(f'No existe la configuracion {APP_ENV}')