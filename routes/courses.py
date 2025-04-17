from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ..models.course import Course  # Changed to relative import
from ..extensions import db  # Changed to relative import

courses = Blueprint('courses', __name__)

@courses.route('/courses')
@login_required
def list():
    if current_user.role == 'teacher':
        courses = Course.query.filter_by(teacher_id=current_user.id).all()
    else:
        courses = Course.query.all()
    return render_template('courses/list.html', courses=courses)

@courses.route('/courses/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role != 'teacher':
        flash('Only teachers can create courses')
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        course = Course(
            title=title,
            description=description,
            teacher_id=current_user.id
        )
        
        db.session.add(course)
        db.session.commit()
        
        return redirect(url_for('courses.list'))
        
    return render_template('courses/create.html')

@courses.route('/courses/<int:id>')
@login_required
def view(id):
    course = Course.query.get_or_404(id)
    return render_template('courses/view.html', course=course)