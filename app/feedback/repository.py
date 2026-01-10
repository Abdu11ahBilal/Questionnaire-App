from app.extensions import db
from app.models.answer import Answer
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

class AnswerRepository:

    @staticmethod
    def save_bulk_answers(answers_data):
        """
        Expects a list of dictionaries:
        [{'user_id': 1, 'question_id': 5, 'answer_value': 'Yes', 'submission_id': 'abc'}, ...]
        """
        try:
            for data in answers_data:
                new_answer = Answer(**data) 
                db.session.add(new_answer)

            db.session.commit()
            logger.info(f"Successfully saved {len(answers_data)} answers.")
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during bulk save: {e}")
            raise e