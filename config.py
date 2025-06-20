# import os
# from dotenv import load_dotenv

# # Carga el archivo .env
# load_dotenv()

# class BaseConfig:
#     SECRET_KEY = os.getenv('SECRET_KEY')
#     FLASK_APP = os.getenv('FLASK_APP')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

# class DevelopmentConfig(BaseConfig):
#     FLASK_ENV = 'development'
#     DEBUG = True
#     DB_USER = os.getenv('DB_USERNAME')
#     DB_PASSWORD = os.getenv('DB_PASSWORD')
#     DB_HOST = os.getenv('DB_HOST')
#     DB_PORT = os.getenv('DB_PORT')
#     DB_NAME = os.getenv('DB_DATABASE')
#     SQLALCHEMY_DATABASE_URI = (
#     f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# class TestingConfig(BaseConfig):
#     FLASK_ENV = 'testing'
#     DEBUG = True
#     TESTING = True
#     # Aquí puedes configurar una base de datos diferente solo para test
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # O crea una base de datos de test

# class ProductionConfig(BaseConfig):
#     FLASK_ENV = 'production'
#     DEBUG = False
#     DB_URI = os.getenv('DATABASE_URL')  # URL completa desde .env
#     SQLALCHEMY_DATABASE_URI = DB_URI
#     SECRET_KEY = os.getenv('PROD_SECRET_KEY')

# -----------nuevo config---------------------------------------
# -----------------------------------------------------------------
# -----------------------------------------------------------------

import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

# Carga el archivo .env
load_dotenv()

def get_env_variable(name, default=None):
    """Obtiene variable de entorno o devuelve default/levanta error"""
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"La variable de entorno {name} no está configurada")
    return value

class BaseConfig:
    SECRET_KEY = get_env_variable('SECRET_KEY')
    FLASK_APP = get_env_variable('FLASK_APP', 'wsgi:app')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600,
    }

class DevelopmentConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    DB_USER = get_env_variable('DB_USER')
    DB_PASSWORD = quote_plus(get_env_variable('DB_PASSWORD'))
    DB_HOST = get_env_variable('DB_HOST')
    DB_PORT = get_env_variable('DB_PORT', '3306')
    DB_NAME = get_env_variable('DB_NAME')
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

class ProductionConfig(BaseConfig):
    FLASK_ENV = 'production'
    DEBUG = False
    # Para producción, es mejor usar una URL completa en una sola variable
    SQLALCHEMY_DATABASE_URI = get_env_variable('DATABASE_URL')
    # Opcional: Sobrescribir SECRET_KEY específica para producción
    SECRET_KEY = get_env_variable('PROD_SECRET_KEY', os.getenv('SECRET_KEY'))

# Configuración por defecto
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': ProductionConfig  # Cambia esto según tu entorno por defecto
}