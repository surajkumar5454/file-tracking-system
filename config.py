import os
from pathlib import Path

basedir = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    
    # Create instance directory if it doesn't exist
    INSTANCE_PATH = os.path.join(basedir, 'instance')
    os.makedirs(INSTANCE_PATH, exist_ok=True)
    
    # Use absolute path for database
    DB_PATH = os.path.join(INSTANCE_PATH, 'file_tracking.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DB_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Create uploads directory if it doesn't exist
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    os.makedirs(UPLOAD_FOLDER, exist_ok=True) 