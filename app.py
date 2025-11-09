# --- Force Redeploy v2 ---
from flask import Flask, render_template
from backend.extensions import db, security, api, migrate
from backend.config import LocalDevelopmentConfig, ProductionConfig
from backend.security import user_datastore
import os
from whitenoise import WhiteNoise
from flask_jwt_extended import JWTManager
import datetime

def createApp():
    """
    Creates and configures the Flask application. This is the app factory.
    """
    # This configuration tells Flask where your static files and templates are,
    # and that they should be served from the root URL path (e.g., /app.js), not /static/app.js.
    app = Flask(__name__,
                static_folder='frontend',
                template_folder='frontend',
                static_url_path='')
    
    # Automatically select the correct configuration based on the environment.
    # Render sets FLASK_ENV=production by default.
    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(LocalDevelopmentConfig)

    # Add JWT configuration
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=24)
    
    # Initialize all Flask extensions
    db.init_app(app)
    api.init_app(app)
    migrate.init_app(app, db)
    security.init_app(app, user_datastore)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Push an application context to make sure extensions can be used
    app.app_context().push()

    # Import the routes after the app is configured
    with app.app_context():
        from backend import routes

    return app

# Create the application instance using the factory
app = createApp()

# Wrap the Flask app with WhiteNoise.
# WhiteNoise will automatically find the `static_folder` ('frontend') from the 
# Flask `app` object and handle serving those files efficiently.
app.wsgi_app = WhiteNoise(app.wsgi_app)

# --- START: RENDER COMMAND CODE ---
#
# THIS ENTIRE BLOCK HAS BEEN REMOVED.
# It was causing the ImportError and crashing the app.
# We are now using the temporary /api/admin/run-db-setup route
# (defined in routes.py) to initialize the database safely after
# the app has started.
#
# --- END: RENDER COMMAND CODE ---

# Health check endpoint
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.datetime.utcnow().isoformat()}

# Database initialization endpoint
@app.route('/api/init-db')
def init_db():
    try:
        db.create_all()
        return {'message': 'Database initialized successfully'}, 200
    except Exception as e:
        return {'error': str(e)}, 500

# This block is only for running the app locally with the Flask development server.
# Gunicorn will not use this when you deploy to Render.
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
