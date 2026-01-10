from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from app.auth.repository import UserRepository
from loguru import logger
from app.extensions import login_manager

@login_manager.user_loader
def load_user(user_id):
    try:
        user = UserRepository.get_by_id(int(user_id))
        return user
    except (ValueError, TypeError):
        return None
    
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')

    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    if not username or not email or not password:
        flash("All fields are required!", "warning")
        return redirect(url_for('auth.signup'))

    try:
        UserRepository.create_user(username, email, password)
        
        logger.info(f"New user registered: {username}")
        flash("Account created! Please log in.", "success")
        return redirect(url_for('auth.login'))

    except ValueError as e:
        flash(str(e), "danger")
        return redirect(url_for('auth.signup'))
    
    except Exception as e:
        logger.error(f"Signup crash: {e}")
        flash("A system error occurred. Try again later.", "danger")
        return redirect(url_for('auth.signup'))
    
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feedback.index')) # Or wherever your home is

    if request.method == 'GET':
        return render_template('auth/login.html')

    email = request.form.get('email')
    password = request.form.get('password')

    user = UserRepository.get_by_email(email)

    if user and UserRepository.verify_password(user, password):
        login_user(user) # This is the magic "Wristband" line
        logger.info(f"User logged in: {user.username}")
        return redirect(url_for('feedback.index'))
    
    flash("Invalid email or password.", "danger")
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required 
def logout():
    logout_user() 
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))