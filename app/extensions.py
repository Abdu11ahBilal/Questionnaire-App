from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from loguru import logger
import sys

db = SQLAlchemy()
login_manager = LoginManager()
logger.remove() 
logger.add(sys.stderr, format="<green>{time}</green> | <level>{level: <8}</level> | <cyan>{message}</cyan>", level="INFO")