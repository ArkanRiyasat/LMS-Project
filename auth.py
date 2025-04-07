from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from extensions import db

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
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('auth.register'))

        new_user = User(
            email=email,
            username=username,
            password=generate_password_hash(password if password is not None else "", method='pbkdf2:sha256'),
            role=role
        )

        db.session.add(new_user)
        db.session.commit()

        # In your register route
        flash(f'Congrats! You have registered as a {role}. Please login to continue.', 'success')
        return redirect(url_for('auth.login_with_role', role=role))

    return render_template('auth/register.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))