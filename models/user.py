from flask_login import UserMixin
from ..extensions import db  # Changed to relative import with double dots

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    is_verified = db.Column(db.Boolean, default=True, nullable=False)  # Changed default to True

    # Add relationships
    courses = db.relationship('Course', backref='teacher', lazy=True, 
                            foreign_keys='Course.teacher_id')

    def get_id(self):
        return str(self.id)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
