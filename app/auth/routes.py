from flask import render_template, request, redirect, session, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from pydantic import ValidationError
from loguru import logger

from . import auth_bp
from app.auth.repository import UserRepository
from app.extensions import login_manager
from .schemas import SignupSchema, LoginSchema

@login_manager.user_loader
def load_user(user_id):
    try:

        return UserRepository.get_by_id(int(user_id))
    except (ValueError, TypeError, Exception) as e:
        logger.error(f"User loader failed for ID {user_id}: {e}")
        return None

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('auth/signup.html')

    try:

        data = SignupSchema(**request.form.to_dict())
        
        UserRepository.create_user(data.username, data.email, data.password)
        
        logger.info(f"Signup success: username='{data.username}' email='{data.email}'")
        flash("Account created! Please log in.", "success")
        return redirect(url_for('auth.login'))

    except ValidationError as e:
        logger.warning(f"Signup validation failure: {e.errors()}")
        flash("Invalid details. Check your input and try again.", "danger")
    except ValueError as e:
        logger.warning(f"Signup rejected (Business Logic): {str(e)}")
        flash(str(e), "danger")
    except Exception as e:
        logger.critical(f"Signup system crash: {e}")
        flash("A system error occurred. Our engineers have been notified.", "danger")
        
    return redirect(url_for('auth.signup'))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('feedback.index'))

    if request.method == 'GET':
        return render_template('auth/login.html')

    try:

        data = LoginSchema(**request.form.to_dict())
        
        user = UserRepository.get_by_email(data.email)

        if user and UserRepository.verify_password(user, data.password):
            login_user(user)
            logger.info(f"Login success: user_id={user.id}")
            return redirect(url_for('feedback.index'))
        
        logger.warning(f"Login failed for email: {data.email}")
        flash("Invalid email or password.", "danger")
        
    except ValidationError:
        logger.warning("Login attempt with malformed data.")
        flash("Please enter a valid email and password.", "danger")
    except Exception as e:
        logger.error(f"Login system error: {e}")
        flash("Temporary login issue. Please try again later.", "danger")
        
    return redirect(url_for('auth.login'))

@auth_bp.route('/logout')
@login_required 
def logout():
    session.pop('feedback_answers', None)
    
    logger.info(f"User {current_user.id} logged out and session cleared.")
    
    logout_user() 
    
    flash("You have been logged out.", "info")
    return redirect(url_for('auth.login'))