import os

class Config:
    SECRET_KEY = 'your-secret-key'  # Change this to a secure secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lms.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False