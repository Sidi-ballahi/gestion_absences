import os
from datetime import timedelta

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/gestion_absences"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Flask-Mail configuration
    # MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    # MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') == 'True' or True
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'gdesabsences@gmail.com'
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'wxcr wmsy bjzi ncmb'
    # MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'gdesabsences@gmail.com'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME', 'gdesabsences@gmail.com')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', 'wxcr wmsy bjzi ncmb')  # ton mot de passe d’application Gmail
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'gdesabsences@gmail.com')

    # Upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
