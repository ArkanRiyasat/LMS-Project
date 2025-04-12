from flask import Flask
from .extensions import db, migrate, login_manager
from .models import User, Course, Assignment
from .config.email_config import mail, EmailConfig

def create_app():
    app = Flask(__name__)
    return app