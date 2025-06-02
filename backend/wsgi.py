"""
WSGI entry point for Railway deployment.
<<<<<<< HEAD
<<<<<<< HEAD
This file imports the Flask app and exposes it for gunicorn.
Updated: 2025-12-13
"""
import sys
import os

# Add current directory to path to ensure proper imports
sys.path.insert(0, os.path.dirname(__file__))

# Import create_app factory
from application import create_app

# Create app with production config
config_name = os.getenv('FLASK_ENV', 'production')
app = create_app(config_name)
=======
This file imports the Flask app from app.py and exposes it for gunicorn.
"""
from app import app
>>>>>>> 8df0d54 (add wsgi entry point)
=======
This file imports the Flask app and exposes it for gunicorn.
Updated: 2025-12-13
"""
import sys
import os

# Add current directory to path to ensure proper imports
sys.path.insert(0, os.path.dirname(__file__))

# Import app from app.py (not the app/ package)
from app import app as application

# Alias for gunicorn
app = application
>>>>>>> 5d772cd (improve wsgi imports)

if __name__ == "__main__":
    application.run()
