import os
from dotenv import load_dotenv

# Load environment variables from a .env file (good for local development)
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_very_secret_default_key_fallback')
    
    # --- Database Configuration ---
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Flask-Security-Too Configuration ---
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'a_very_secret_salt_fallback')
    
    # We are moving this setting into the classes below to be more explicit
    # SECURITY_TOKEN_MAX_AGE = 86400 

    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    WTF_CSRF_ENABLED = False
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True


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

    # --- THIS IS THE FIX ---
    # We've added the setting directly here to ensure it is read.
    SECURITY_TOKEN_MAX_AGE = 86400 # 24 hours in seconds


class LocalDevelopmentConfig(Config):
    """Local development configuration."""
    DEBUG = True
    # The .env file should contain:
    # DATABASE_URL="sqlite:///./instance/local.db"
    # This will create a local.db file in an 'instance' folder.
    
    # --- THIS IS THE FIX ---
    # We've added the setting directly here to ensure it is read.
    SECURITY_TOKEN_MAX_AGE = 86400 # 24 hours in seconds
