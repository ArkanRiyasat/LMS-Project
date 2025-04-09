import os

class Config:
    SECRET_KEY = 'your-secret-key-here'
    # Update this line with your MySQL password
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:2005@localhost/lms'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload configuration
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
