from app import create_app
from extensions import db

app = create_app()

with app.app_context():
    # Drop all existing tables
    db.drop_all()
    # Create all tables
    db.create_all()
    print("Database tables created successfully!")