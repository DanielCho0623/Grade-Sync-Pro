import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    jwt.init_app(app)

    # CORS configuration - allows both local and production origins
    allowed_origins = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:5001"
    ]

    # Add production frontend URL from environment variable
    frontend_url = os.getenv('FRONTEND_URL')
    if frontend_url:
        allowed_origins.append(frontend_url)
        # Also allow the URL without trailing slash and with https
        allowed_origins.append(frontend_url.rstrip('/'))
        if frontend_url.startswith('http://'):
            allowed_origins.append(frontend_url.replace('http://', 'https://'))

    CORS(app, resources={
        r"/api/*": {
            "origins": allowed_origins,
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        app.logger.error(f"Invalid token: {error_string}")
        return {'error': 'Invalid token', 'details': error_string}, 422

    @jwt.unauthorized_loader
    def unauthorized_callback(error_string):
        app.logger.error(f"Unauthorized: {error_string}")
        return {'error': 'Missing authorization header', 'details': error_string}, 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        app.logger.error(f"Expired token")
        return {'error': 'Token has expired'}, 401

    from application.routes.auth import auth_bp
    from application.routes.courses import courses_bp
    from application.routes.grades import grades_bp
    from application.routes.notifications import notifications_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    app.register_blueprint(grades_bp, url_prefix='/api/grades')
    app.register_blueprint(notifications_bp, url_prefix='/api/notifications')

    with app.app_context():
        # Import models to register them with SQLAlchemy before creating tables
        from application import models
        db.create_all()

    return app
