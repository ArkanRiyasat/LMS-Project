from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()

# Configure login manager
login_manager.login_view = 'auth.login_with_role'
login_manager.login_message = 'Please log in to access this page.'

def init_app(app):
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)