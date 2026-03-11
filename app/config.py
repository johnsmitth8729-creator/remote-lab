import os
from datetime import timedelta

class Config:
    # Basic Config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Database Config
    # Default to SQLite for local development, but ready for Postgres
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///remote_lab.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT Config
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-67890')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_COOKIE_NAME = "jwt_token"
    
    # Babel Config
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_SUPPORTED_LOCALES = ['en', 'uz', 'ru']
    BABEL_TRANSLATION_DIRECTORIES = 'translations'

    # Security
    BCRYPT_LOG_ROUNDS = 13
