import os

""" Should use dotenv configuration etc to load in the secret key and other security critical environment variables """




class Config():

    """ Base configuration os.environ.get looks for the environment variable, if not found then use default of secret key"""
    SECRET_KEY = os.environ.get('CONDUIT_SECRET', 'secret-key')  # TODO: Change me
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/flask_silver_app_dev"

    CACHE_TYPE = "simple"


    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_NAME = 'access_token_cookie'
    JWT_COOKIE_CSRF_PROTECT = True




class DevConfig(Config):

    ENV = "dev"
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/flask_silver_app_dev"
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
