from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from loguru import logger
import sys

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login' # type: ignore
login_manager.login_message_category = 'info'
logger.remove() 
logger.add(sys.stderr, format="<green>{time}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>", level="INFO")