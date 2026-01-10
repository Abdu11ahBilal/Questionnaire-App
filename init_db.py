from app import create_app
from app.extensions import db
# Crucial: Import your models so SQLAlchemy "sees" them
from app.models.user import User
from app.models.answer import Answer

app = create_app()

with app.app_context():
    print("Dropping all tables...")
    db.drop_all()  # Clear out that manual file you made
    
    print("Creating all tables...")
    db.create_all()
    
    print("Success! Check your /instance folder.")