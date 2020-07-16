''' Flask config '''

from os import environ, path

basedir = path.abspath(path.dirname(__file__))

class BaseConfig:
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_VERSION = 'v1'
    

class DevConfig(BaseConfig):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True

    SQLALCHEMY_ECHO = True
    

class ProdConfig(BaseConfig):
    FLASK_ENV = 'production'
    DEBUG = True
    TESTING = False

    SQLALCHEMY_ECHO = False