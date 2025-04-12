from flask import Flask, render_template, redirect, url_for
from flask_login import current_user, login_required
from extensions import db, migrate, login_manager, mail
from models import User, Course, Assignment
from routes.auth import auth
from routes.courses import courses
from routes.assignments import assignments
from routes.profile import profile
from config.config import Config  # Updated import

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(courses)
    app.register_blueprint(assignments)
    app.register_blueprint(profile)
    
    # Define routes
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
            pending_submissions = 0
            recent_submissions = []
            
            return render_template('teacher/dashboard.html',
                                courses=courses,
                                courses_count=courses_count,
                                students_count=students_count,
                                pending_submissions=pending_submissions,
                                recent_submissions=recent_submissions)
        else:
            enrolled_courses = Course.query.all()
            assignments = Assignment.query.all()
            return render_template('student/dashboard.html',
                                courses=enrolled_courses,
                                assignments=assignments)
    
    return app

# Create the app instance
app = create_app()
app.app_context().push()

if __name__ == '__main__':
    app.run(debug=True)
