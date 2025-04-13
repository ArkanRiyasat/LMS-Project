from flask import Flask
from config.config import Config
from extensions import init_app, db, mail
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure email config is loaded
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')
    
    # Print email config (for debugging)
    print("\nEmail Configuration:")
    print("Mail Server:", app.config.get('MAIL_SERVER'))
    print("Mail Port:", app.config.get('MAIL_PORT'))
    print("Mail Username:", app.config.get('MAIL_USERNAME'))
    print("TLS:", app.config.get('MAIL_USE_TLS'))
    print("Password set:", bool(app.config.get('MAIL_PASSWORD')))
    print()
    
    # Initialize extensions
    init_app(app)  # Use the init_app function from extensions.py
    
    # Register blueprints
    from routes.auth import auth
    app.register_blueprint(auth)
    
    return app