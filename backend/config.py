import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

    # Railway uses postgres:// but SQLAlchemy 1.4+ requires postgresql://
    database_url = os.getenv('DATABASE_URL', 'postgresql://localhost/gradesync')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BRIGHTSPACE_URL = os.getenv('BRIGHTSPACE_URL', '')
    BRIGHTSPACE_CLIENT_ID = os.getenv('BRIGHTSPACE_CLIENT_ID', '')
    BRIGHTSPACE_CLIENT_SECRET = os.getenv('BRIGHTSPACE_CLIENT_SECRET', '')

    GMAIL_CREDENTIALS_PATH = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials/gmail_credentials.json')
    GMAIL_TOKEN_PATH = os.getenv('GMAIL_TOKEN_PATH', 'credentials/gmail_token.json')

    OUTLOOK_CLIENT_ID = os.getenv('OUTLOOK_CLIENT_ID', '')
    OUTLOOK_CLIENT_SECRET = os.getenv('OUTLOOK_CLIENT_SECRET', '')
    OUTLOOK_TENANT_ID = os.getenv('OUTLOOK_TENANT_ID', '')

    ALERT_EMAIL = os.getenv('ALERT_EMAIL', '')
    GRADE_THRESHOLD = float(os.getenv('GRADE_THRESHOLD', '85.0'))

    USE_SYNTHETIC_DATA = os.getenv('USE_SYNTHETIC_DATA', 'false').lower() == 'true'

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/gradesync_test'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
