from app.extensions import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from loguru import logger

class UserRepository:
    
    @staticmethod
    def create_user(username, email, password):
        hashed_pw = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email, 
            password_hash=hashed_pw
        )
        
        try:
            db.session.add(new_user)
            db.session.commit()
            logger.info(f"User created: {username}")
            return new_user
        except IntegrityError:
            db.session.rollback()
            logger.warning(f"Failed to create user: {username} (Duplicate data)")
            raise ValueError("Username or Email already exists.")

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def get_by_email(email):
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def verify_password(user, password):
        return check_password_hash(user.password_hash, password)