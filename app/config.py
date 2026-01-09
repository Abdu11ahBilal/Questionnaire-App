import os 
class Config:
    SECRET_KEY = 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.dirname(__file__), '..', 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False