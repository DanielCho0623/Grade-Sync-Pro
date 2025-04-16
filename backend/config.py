import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
<<<<<<< HEAD
<<<<<<< HEAD
=======
    """Base configuration"""
>>>>>>> b083b2d (set up flask backend with postgresql)
=======
>>>>>>> 4990274 (clean up code)
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

<<<<<<< HEAD
<<<<<<< HEAD
    # Railway uses postgres:// but SQLAlchemy 1.4+ requires postgresql://
    database_url = os.getenv('DATABASE_URL', 'postgresql://localhost/gradesync')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

=======
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/gradesync')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Brightspace API
>>>>>>> b083b2d (set up flask backend with postgresql)
=======
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/gradesync')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

>>>>>>> 4990274 (clean up code)
    BRIGHTSPACE_URL = os.getenv('BRIGHTSPACE_URL', '')
    BRIGHTSPACE_CLIENT_ID = os.getenv('BRIGHTSPACE_CLIENT_ID', '')
    BRIGHTSPACE_CLIENT_SECRET = os.getenv('BRIGHTSPACE_CLIENT_SECRET', '')

<<<<<<< HEAD
<<<<<<< HEAD
    GMAIL_CREDENTIALS_PATH = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials/gmail_credentials.json')
    GMAIL_TOKEN_PATH = os.getenv('GMAIL_TOKEN_PATH', 'credentials/gmail_token.json')

=======
    # Gmail API
    GMAIL_CREDENTIALS_PATH = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials/gmail_credentials.json')
    GMAIL_TOKEN_PATH = os.getenv('GMAIL_TOKEN_PATH', 'credentials/gmail_token.json')

    # Outlook API
>>>>>>> b083b2d (set up flask backend with postgresql)
=======
    GMAIL_CREDENTIALS_PATH = os.getenv('GMAIL_CREDENTIALS_PATH', 'credentials/gmail_credentials.json')
    GMAIL_TOKEN_PATH = os.getenv('GMAIL_TOKEN_PATH', 'credentials/gmail_token.json')

>>>>>>> 4990274 (clean up code)
    OUTLOOK_CLIENT_ID = os.getenv('OUTLOOK_CLIENT_ID', '')
    OUTLOOK_CLIENT_SECRET = os.getenv('OUTLOOK_CLIENT_SECRET', '')
    OUTLOOK_TENANT_ID = os.getenv('OUTLOOK_TENANT_ID', '')

<<<<<<< HEAD
<<<<<<< HEAD
    ALERT_EMAIL = os.getenv('ALERT_EMAIL', '')
    GRADE_THRESHOLD = float(os.getenv('GRADE_THRESHOLD', '85.0'))

    USE_SYNTHETIC_DATA = os.getenv('USE_SYNTHETIC_DATA', 'false').lower() == 'true'

class DevelopmentConfig(Config):
=======
    # Notification Settings
=======
>>>>>>> 4990274 (clean up code)
    ALERT_EMAIL = os.getenv('ALERT_EMAIL', '')
    GRADE_THRESHOLD = float(os.getenv('GRADE_THRESHOLD', '85.0'))

class DevelopmentConfig(Config):
<<<<<<< HEAD
    """Development configuration"""
>>>>>>> b083b2d (set up flask backend with postgresql)
=======
>>>>>>> 4990274 (clean up code)
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
<<<<<<< HEAD
<<<<<<< HEAD
=======
    """Production configuration"""
>>>>>>> b083b2d (set up flask backend with postgresql)
=======
>>>>>>> 4990274 (clean up code)
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
<<<<<<< HEAD
<<<<<<< HEAD
=======
    """Testing configuration"""
>>>>>>> b083b2d (set up flask backend with postgresql)
=======
>>>>>>> 4990274 (clean up code)
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/gradesync_test'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
