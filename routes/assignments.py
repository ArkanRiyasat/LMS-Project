from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.assignment import Assignment
from models.course import Course
from extensions import db
from datetime import datetime

assignments = Blueprint('assignments', __name__)

@assignments.route('/assignments/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.role != 'teacher':
        flash('Only teachers can create assignments')
        return redirect(url_for('dashboard'))
    
    courses = Course.query.filter_by(teacher_id=current_user.id).all()
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        due_date_str = request.form.get('due_date')
        if due_date_str is None:
            flash('Due date is required')
            return redirect(url_for('assignments.create'))
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        course_id = request.form.get('course_id')
        
        assignment = Assignment(
            title=title,
            description=description,
            due_date=due_date,
            course_id=course_id
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        return redirect(url_for('assignments.list'))
        
    return render_template('assignments/create.html', courses=courses)

@assignments.route('/assignments')
@login_required
def list():
    if current_user.role == 'teacher':
        assignments = Assignment.query.join(Course).filter(Course.teacher_id == current_user.id).all()
    else:
        assignments = Assignment.query.all()
    return render_template('assignments/list.html', assignments=assignments)

@assignments.route('/assignments/submissions')
@login_required
def submissions():
    if current_user.role == 'teacher':
        return render_template('assignments/submissions.html', submissions=[])  # Will be implemented later
    else:
        return redirect(url_for('assignments.list'))

@assignments.route('/assignments/grade/<int:id>')
@login_required
def grade(id):
    if current_user.role != 'teacher':
        flash('Only teachers can grade assignments')
        return redirect(url_for('dashboard'))
    return render_template('assignments/grade.html')  # Will be implemented later