from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from extensions import db, mail
from flask import current_app
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from extensions import mail  # Remove this duplicate
from config.email_config import mail  # Remove this
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

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        email = request.form.get('email')
        username = request.form.get('username')
        phone = request.form.get('phone')
        password = request.form.get('password')
        role = request.form.get('role')
        captcha_input = request.form.get('captcha')

        print("Form data received:", {  # Debug print
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'username': username,
            'phone': phone,
            'role': role,
            'captcha_input': captcha_input,
            'stored_captcha': session.get('captcha_code')
        })

        # Validate CAPTCHA
        if not captcha_input or captcha_input != session.get('captcha_code'):
            print(f"CAPTCHA validation failed: Input={captcha_input}, Stored={session.get('captcha_code')}")  # Debug print
            flash('Invalid CAPTCHA code', 'error')
            return redirect(url_for('auth.register'))

        if not all([first_name, last_name, email, username, password, role]):
            print("Missing required fields:", {  # Debug print
                'first_name': bool(first_name),
                'last_name': bool(last_name),
                'email': bool(email),
                'username': bool(username),
                'password': bool(password),
                'role': bool(role)
            })
            flash('All fields are required', 'error')
            return redirect(url_for('auth.register'))

        # Check if phone number exists
        existing_phone = User.query.filter_by(phone=phone).first()
        if existing_phone:
            flash('Phone number already registered', 'error')
            return redirect(url_for('auth.register'))

        # Check if user exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            if not existing_user.is_verified:
                # User exists but not verified, send new verification code
                session['user_id'] = existing_user.id
                session['user_email'] = email
                code = send_email_verification(email)
                session['verification_code'] = code
                session['code_timestamp'] = datetime.now().timestamp()
                flash('Please verify your email address', 'info')
                return redirect(url_for('auth.verify'))
            else:
                return redirect(url_for('auth.login_with_role', role=existing_user.role))

        # Create new user if doesn't exist
        try:
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
            
            # Send verification email
            send_verification_email(new_user)
            flash('Registration successful! Please check your email to verify your account.', 'success')
            
            return redirect(url_for('auth.login_with_role', role=role))
        except Exception as e:
            print("Registration error:", str(e))
            db.session.rollback()
            flash('Registration failed. Please try again.', 'error')
            return redirect(url_for('auth.register'))

    # GET request - render registration form
    return render_template('auth/register.html')

@auth.route('/verify', methods=['GET', 'POST'])
def verify():
    user_email = session.get('user_email')
    print(f"Verify route accessed for email: {user_email}")  # Debug print
    print(f"Session data: {dict(session)}")  # Debug print
    
    if not user_email:
        flash('No email found. Please register again.', 'error')
        return redirect(url_for('auth.register'))
    
    return render_template('auth/verify.html', user_email=user_email)

@auth.route('/verify/resend', methods=['POST'])
def resend_code():
    user_email = session.get('user_email')
    if not user_email:
        return jsonify({'error': 'No email found'}), 400
        
    code = send_email_verification(user_email)
    session['verification_code'] = code
    session['code_timestamp'] = datetime.now().timestamp()
    
    return jsonify({'message': 'Verification code resent to your email'})

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


def send_verification_email(user):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    token = serializer.dumps(user.email, salt='email-verification-salt')
    
    msg = Message('Verify Your Email',
                  recipients=[user.email])
    
    verification_url = url_for('auth.verify_email', 
                             token=token, 
                             _external=True)
    
    msg.body = f'''Please click the following link to verify your email:
    {verification_url}
    
    If you did not create an account, please ignore this email.
    '''
    
    mail.send(msg)

@auth.route('/verify-email/<token>')
def verify_email(token):
    try:
        serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        email = serializer.loads(token, 
                               salt='email-verification-salt',
                               max_age=3600)  # Token expires in 1 hour
        user = User.query.filter_by(email=email).first()
        if user:
            user.email_verified = True
            db.session.commit()
            flash('Your email has been verified!', 'success')
            return redirect(url_for('auth.login'))
    except:
        flash('The verification link is invalid or has expired.', 'error')
    return redirect(url_for('auth.login'))
