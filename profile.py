from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from extensions import db

profile = Blueprint('profile', __name__)

@profile.route('/profile')
@login_required
def view():
    return render_template('profile/view.html')

@profile.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')

        if current_password and new_password:
            if check_password_hash(current_user.password, current_password):
                current_user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            else:
                flash('Current password is incorrect')
                return redirect(url_for('profile.edit'))

        current_user.username = username
        current_user.email = email
        
        db.session.commit()
        flash('Profile updated successfully')
        return redirect(url_for('profile.view'))

    return render_template('profile/edit.html')