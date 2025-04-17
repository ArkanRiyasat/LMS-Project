from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User
from ..models.course import Course
from ..models.assignment import Assignment
from ..extensions import db

profile = Blueprint('profile', __name__)

@profile.route('/profile')
@login_required
def view_profile():
    stats = {}
    if current_user.role == 'teacher':
        stats = {
            'courses_count': Course.query.filter_by(teacher_id=current_user.id).count(),
            'students_count': User.query.filter_by(role='student').count(),
            'pending_submissions': Assignment.query.filter_by(
                teacher_id=current_user.id,
                status='submitted'
            ).count()
        }
    else:
        stats = {
            'enrolled_courses': Course.query.join(Course.students).filter(User.id == current_user.id).count(),
            'completed_assignments': Assignment.query.filter_by(
                student_id=current_user.id,
                status='completed'
            ).count(),
            'pending_assignments': Assignment.query.filter_by(
                student_id=current_user.id,
                status='pending'
            ).count()
        }
    return render_template('profile/view.html', stats=stats)

@profile.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        bio = request.form.get('bio')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')

        if not username or not email:
            flash('Username and email are required!', 'error')
            return redirect(url_for('profile.edit'))

        # Check if username is taken by another user
        existing_user = User.query.filter(
            User.username == username,
            User.id != current_user.id
        ).first()
        if existing_user:
            flash('Username is already taken!', 'error')
            return redirect(url_for('profile.edit'))

        if current_password and new_password:
            if check_password_hash(current_user.password, current_password):
                current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
                flash('Password updated successfully!', 'success')
            else:
                flash('Current password is incorrect!', 'error')
                return redirect(url_for('profile.edit'))

        current_user.username = username
        current_user.email = email
        current_user.bio = bio
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.view_profile'))

    return render_template('profile/edit.html')