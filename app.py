# --- Force Redeploy v2 ---
from flask import Flask, render_template, send_from_directory
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
    app = Flask(__name__,
                static_folder='frontend',
                template_folder='frontend',
                static_url_path='')
    
    # Automatically select the correct configuration based on the environment.
    if os.environ.get('FLASK_ENV') == 'production':
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(LocalDevelopmentConfig)

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
app.wsgi_app = WhiteNoise(app.wsgi_app)

# 🚨 CRITICAL FIX: Remove duplicate route definitions
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_vue_app(path):
    """
    Serve the Vue.js application for all routes.
    This allows Vue Router to handle client-side routing.
    """
    # Serve static files (JS, CSS, images, etc.)
    if path and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    
    # For all other routes, serve index.html (Vue Router will handle the rest)
    return send_from_directory(app.static_folder, 'index.html')

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
