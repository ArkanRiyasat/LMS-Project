from flask import Flask, render_template, redirect, url_for
from flask_login import current_user, login_required
from extensions import db, migrate, login_manager
from models import User, Course, Assignment
from routes import auth, courses, assignments, profile
from config import Config
from flask_assets import Environment, Bundle

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    # Removed mail.init_app(app)
    
    # Setup Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(courses)
    app.register_blueprint(assignments)
    app.register_blueprint(profile)
    
    @app.route('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('auth.select_role'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'teacher':
            courses = Course.query.filter_by(teacher_id=current_user.id).all()
            courses_count = len(courses)
            students_count = User.query.filter_by(role='student').count()
            # Get recent submissions
            recent_submissions = Assignment.query.filter_by(teacher_id=current_user.id)\
                .order_by(Assignment.created_at.desc())\
                .limit(5)\
                .all()
            return render_template('teacher/dashboard.html',
                                courses=courses,
                                courses_count=courses_count,
                                students_count=students_count,
                                pending_submissions=0,
                                recent_submissions=recent_submissions)
        else:
            courses = Course.query.all()  # Or filter by enrolled courses
            assignments = Assignment.query.all()  # Or filter by student's assignments
            return render_template('student/dashboard.html',
                                courses=courses,
                                assignments=assignments)
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
