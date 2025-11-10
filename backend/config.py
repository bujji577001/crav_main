import os
from dotenv import load_dotenv

# Load environment variables from a .env file (good for local development)
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_default_key_fallback')
    
    # --- Database Configuration ---
    # 🚨 CRITICAL FIX: Handle PostgreSQL URL format for Render
    database_url = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Flask-Security-Too Configuration ---
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'a_very_secret_salt_fallback')
    
    # We use a token-based authentication system
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    
    # Disable CSRF for our stateless API
    WTF_CSRF_ENABLED = False
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True

    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 hours in seconds


class ProductionConfig(Config):
    """Production configuration (used by Render)."""
    # Ensure a strong, unique secret key is set in Render's environment variables
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for production app")

    # Ensure a unique salt is set
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT')
    if not SECURITY_PASSWORD_SALT:
        raise ValueError("No SECURITY_PASSWORD_SALT set for production app")

    # JWT Configuration for production
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    if not JWT_SECRET_KEY:
        raise ValueError("No JWT_SECRET_KEY set for production app")

    # 🚨 IMPORTANT: Disable debug mode in production
    DEBUG = False
    TESTING = False


class LocalDevelopmentConfig(Config):
    """Local development configuration."""
    DEBUG = True
    # The .env file should contain:
    # DATABASE_URL="sqlite:///./instance/local.db"
    # This will create a local.db file in an 'instance' folder.
