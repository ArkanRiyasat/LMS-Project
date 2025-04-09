from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User  # Change from relative to absolute import
from extensions import db  # Change from relative to absolute import

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
            flash('Please check your login details and try again.')
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

        # Validate required fields
        if not all([first_name, last_name, email, username, phone, password, role]):
            flash('All fields are required', 'error')
            return redirect(url_for('auth.register'))

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('auth.register'))

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            phone=phone,
            password=generate_password_hash(password if password is not None else "", method='pbkdf2:sha256'),
            role=role
        )

        try:
            db.session.add(new_user)
            db.session.commit()
            flash(f'Congrats! You have registered as a {role}. Please login to continue.', 'success')
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