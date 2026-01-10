from app import create_app
from app.extensions import db
from app.auth.repository import UserRepository
from app.feedback.repository import AnswerRepository
from app.models.user import User

app = create_app()

with app.app_context():
    # 1. Clean the slate (Careful: this wipes the DB!)
    db.drop_all()
    db.create_all()
    print("✅ Database reset.")

    # 2. Test: Create a User
    try:
        user = UserRepository.create_user("test_pilot", "test@example.com", "password123")
        print(f"✅ User created: {user.username}")
    except Exception as e:
        print(f"❌ Failed to create user: {e}")

    # 3. Test: Duplicate User (This SHOULD fail)
    try:
        UserRepository.create_user("test_pilot", "test@example.com", "different_pass")
    except ValueError as e:
        print(f"✅ Correctly caught duplicate: {e}")

    # 4. Test: Bulk Save Answers
    try:
        # We need the user's ID we just created
        user = UserRepository.get_by_username("test_pilot")
        if user is None:
            raise ValueError("User not found")
        user_id = user.id
        
        dummy_answers = [
            {'user_id': user_id, 'submission_id': 'batch_1', 'question_id': 1, 'answer_value': 'Great!'},
            {'user_id': user_id, 'submission_id': 'batch_1', 'question_id': 2, 'answer_value': 'Maybe.'}
        ]
        
        AnswerRepository.save_bulk_answers(dummy_answers)
        print("✅ Bulk answers saved successfully.")
    except Exception as e:
        print(f"❌ Failed to save answers: {e}")