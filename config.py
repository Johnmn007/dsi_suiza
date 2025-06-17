import os
from dotenv import load_dotenv

# Carga el archivo .env
load_dotenv()

class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY')
    FLASK_APP = os.getenv('FLASK_APP')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    DB_USER = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_HOST = os.getenv('DB_HOST')
    DB_PORT = os.getenv('DB_PORT')
    DB_NAME = os.getenv('DB_DATABASE')
    SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

class TestingConfig(BaseConfig):
    FLASK_ENV = 'testing'
    DEBUG = True
    TESTING = True
    # Aquí puedes configurar una base de datos diferente solo para test
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # O crea una base de datos de test

class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'
    DEBUG = False
    DB_URI = os.getenv('DATABASE_URL')  # URL completa desde .env
    SQLALCHEMY_DATABASE_URI = DB_URI
    SECRET_KEY = os.getenv('PROD_SECRET_KEY')

