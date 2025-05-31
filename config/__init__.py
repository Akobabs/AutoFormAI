import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Compute the base directory of the project (where run.py is located)
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Ensure the app/data directory exists
DB_DIR = os.path.join(BASE_DIR, 'app', 'data')
os.makedirs(DB_DIR, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'

class DevelopmentConfig(Config):
    DEBUG = True
    # Use an absolute path for the database URI
    DEV_DB_PATH = os.path.join(DB_DIR, 'autocomplete_dev.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or f'sqlite:///{DEV_DB_PATH}'

class ProductionConfig(Config):
    DEBUG = False
    PROD_DB_PATH = os.path.join(DB_DIR, 'autocomplete.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{PROD_DB_PATH}'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}