''' Flask config '''

from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class BaseConfig:
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True

    SQLALCHEMY_DATABASE_URI = 'sqlite:///local.db'
    SQLALCHEMY_ECHO = True
    

class ProdConfig(BaseConfig):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False