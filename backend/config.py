import os
from dotenv import load_dotenv

# Load environment variables from a .env file (good for local development)
load_dotenv()

class Config:
    """Base configuration."""
    # --- MODIFIED: Removed hardcoded secret fallbacks to enforce env vars ---
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    
    # --- Database Configuration ---
    # 🚨 CRITICAL FIX: Handle PostgreSQL URL format for Render
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Flask-Security-Too Configuration ---
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') # MODIFIED
    
    # We use a token-based authentication system
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    
    # Disable CSRF for our stateless API
    WTF_CSRF_ENABLED = False
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True

    # --- 💡 START OF FIX: Force Stateless (Token) Authentication ---
    # Tell Flask-Security to ONLY use token authentication.
    SECURITY_AUTH_MEANS = ["token"]
    
    # When an unauthorized request comes in, return a JSON error
    # instead of redirecting to an HTML login page.
    SECURITY_REDIRECT_BEHAVIOR = "json"
    
    # Disable the "view" that it tries to redirect to.
    SECURITY_UNAUTHORIZED_VIEW = None
    # --- 💡 END OF FIX ---


class ProductionConfig(Config):
    """Production configuration (used by Render)."""
    # Ensure a strong, unique secret key is set in Render's environment variables
    # We rely on the parent class check now.
    if not Config.SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production app")

    # Ensure a unique salt is set
    if not Config.SECURITY_PASSWORD_SALT:
        raise ValueError("No SECURITY_PASSWORD_SALT set for production app")

    # 🚨 IMPORTANT: Disable debug mode in production
    DEBUG = False
    TESTING = False


class LocalDevelopmentConfig(Config):
    """Local development configuration."""
    DEBUG = True
    # The .env file should contain:
    # DATABASE_URL="sqlite:///./instance/local.db"
    # This will create a local.db file in an 'instance' folder.
