from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from extensions import db, mail
from flask import current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime
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
            if not user.is_verified:
                flash('Please verify your email first', 'warning')
                return redirect(url_for('auth.verify'))
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')
    return render_template('auth/login.html', role=role)

def send_verification_email(user):
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = serializer.dumps(user.email, salt='email-verification-salt')
        
        msg = Message('Verify Your Email',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[user.email])
        
        verification_url = url_for('auth.verify_email', 
                                token=token, 
                                _external=True)
        
        msg.body = f'''Please click the following link to verify your email:
        {verification_url}
        
        If you did not create an account, please ignore this email.
        '''
        
        print(f"Sending email to: {user.email}")  # Debug print
        print(f"Using SMTP server: {current_app.config['MAIL_SERVER']}")  # Debug print
        mail.send(msg)
        print("Email sent successfully")  # Debug print
        
    except Exception as e:
        print(f"Detailed email error: {str(e)}")  # More detailed error
        raise

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

        existing_phone = User.query.filter_by(phone=phone).first()
        if existing_phone:
            flash('Phone number already registered', 'error')
            return redirect(url_for('auth.register'))

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            if not existing_user.is_verified:
                send_verification_email(existing_user)
                session['verification_email'] = email
                flash('Please verify your email address', 'info')
                return redirect(url_for('auth.verify'))
            else:
                return redirect(url_for('auth.login_with_role', role=existing_user.role))

        try:
            print("Starting registration process...")  # Debug print
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=username,
                phone=phone,
                password=generate_password_hash(password if password is not None else "", method='pbkdf2:sha256'),
                role=role,
                is_verified=False
            )
            
            db.session.add(new_user)
            db.session.commit()
            print(f"User {email} created successfully")  # Debug print
            
            try:
                print("Attempting to send verification email...")  # Debug print
                send_verification_email(new_user)
                print("Verification email sent successfully")  # Debug print
            except Exception as mail_error:
                print(f"Email error: {str(mail_error)}")  # Debug print
                # Continue even if email fails
            
            session['verification_email'] = email
            print(f"Email {email} stored in session")  # Debug print
            
            flash('Please check your email to verify your account.', 'info')
            print("Redirecting to verification page...")  # Debug print
            return redirect(url_for('auth.verify', _external=True))
            
        except Exception as e:
            print(f"Registration error: {str(e)}")  # Debug print
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            return redirect(url_for('auth.register'))

    return render_template('auth/register.html')

@auth.route('/verify')
def verify():
    print("Verify route accessed")  # Debug print
    user_email = session.get('verification_email')
    print(f"Email from session: {user_email}")  # Debug print
    
    if not user_email:
        print("No email found in session")  # Debug print
        flash('Please register first.', 'error')
        return redirect(url_for('auth.register'))
    
    return render_template('auth/verify.html', user_email=user_email)

@auth.route('/verify-email/<token>')
def verify_email(token):
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(token, 
                               salt='email-verification-salt',
                               max_age=3600)  # Token expires in 1 hour
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_verified = True
            db.session.commit()
            flash('Your email has been verified!', 'success')
            return redirect(url_for('auth.login_with_role', role=user.role))
    except:
        flash('The verification link is invalid or has expired.', 'error')
    return redirect(url_for('auth.login'))

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
    verified_users = User.query.filter_by(is_verified=True).count()
    unverified_users = User.query.filter_by(is_verified=False).count()
    
    users_by_role = {
        'student': User.query.filter_by(role='student').count(),
        'teacher': User.query.filter_by(role='teacher').count()
    }
    
    verified_by_role = {
        'student': User.query.filter_by(role='student', is_verified=True).count(),
        'teacher': User.query.filter_by(role='teacher', is_verified=True).count()
    }
    
    return render_template('auth/user_stats.html',
                         total_users=total_users,
                         verified_users=verified_users,
                         unverified_users=unverified_users,
                         users_by_role=users_by_role,
                         verified_by_role=verified_by_role)


@auth.route('/test-email')
def test_email():
    try:
        msg = Message('Test Email',
                    sender=current_app.config['MAIL_USERNAME'],
                    recipients=[current_app.config['MAIL_USERNAME']])
        msg.body = 'This is a test email.'
        mail.send(msg)
        return 'Email sent successfully!'
    except Exception as e:
        return f'Error sending email: {str(e)}'
