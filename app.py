from flask import Flask, render_template, redirect, url_for
from flask_login import current_user, login_required
from extensions import db, login_manager
from models import User, Course, Assignment

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from auth import auth
    from courses import courses
    from assignments import assignments
    from profile import profile
    
    app.register_blueprint(auth)
    app.register_blueprint(courses)
    app.register_blueprint(assignments)
    app.register_blueprint(profile)

    @app.route('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))
        return redirect(url_for('auth.select_role'))
        return render_template('index.html')

    @app.route('/dashboard')
    @login_required
    def dashboard():
        if current_user.role == 'teacher':
            courses = Course.query.filter_by(teacher_id=current_user.id).all()
            courses_count = len(courses)
            students_count = User.query.filter_by(role='student').count()
            pending_submissions = 0  # Will be implemented later
            recent_submissions = []  # Will be implemented later
            
            return render_template('teacher/dashboard.html',
                                courses=courses,
                                courses_count=courses_count,
                                students_count=students_count,
                                pending_submissions=pending_submissions,
                                recent_submissions=recent_submissions)
        else:
            enrolled_courses = Course.query.all()  # Will be updated with enrollment system
            assignments = Assignment.query.all()  # Will be filtered by student's courses
            return render_template('student/dashboard.html',
                                courses=enrolled_courses,
                                assignments=assignments)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)