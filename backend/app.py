<<<<<<< HEAD
import os
from application import create_app

# Use environment variable for config, default to development
config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    # Get port from environment variable for Railway deployment
    port = int(os.getenv('PORT', 5001))
    # Debug mode based on environment
    debug = config_name == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
=======
from app import create_app

app = create_app('development')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
>>>>>>> 22c8b51 (backend deployment config and tests)
