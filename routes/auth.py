from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.user import User  # Changed to relative import
from ..extensions import db  # Changed to relative import
import random

auth = Blueprint('auth', __name__)

@auth.route('/select-role')
def select_role():
    return render_template('auth/select_role.html')

@auth.route('/login/<role>', methods=['GET', 'POST'])
def login_with_role(role):
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, role=role).first()
        
        if user and password and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('auth/login.html', role=role)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        username = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')
        role = request.form.get('role')
        captcha_input = request.form.get('captcha')

        if not captcha_input or captcha_input != session.get('captcha_code'):
            flash('Invalid CAPTCHA code', 'error')
            return redirect(url_for('auth.register'))

        if not all([first_name, last_name, email, username, password, role]):
            flash('All fields are required', 'error')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already registered', 'error')
            return redirect(url_for('auth.login_with_role', role=role))

        try:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                phone=phone,
                password=generate_password_hash(password, method='pbkdf2:sha256'),
                role=role
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('auth.login_with_role', role=role))
            
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@auth.route('/generate-captcha', methods=['GET'])
def generate_captcha():
    captcha_code = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=6))
    session['captcha_code'] = captcha_code
    return jsonify({'code': captcha_code})

@auth.route('/validate-captcha', methods=['POST'])
def validate_captcha():
    user_input = request.json.get('captcha')
    stored_code = session.get('captcha_code')
    
    if user_input and stored_code and user_input.upper() == stored_code:
        return jsonify({'valid': True})
    return jsonify({'valid': False})

@auth.route('/user-stats')
def user_stats():
    total_users = User.query.count()
    users_by_role = {
        'student': User.query.filter_by(role='student').count(),
        'teacher': User.query.filter_by(role='teacher').count()
    }
    
    return render_template('auth/user_stats.html',
                         total_users=total_users,
                         users_by_role=users_by_role)
