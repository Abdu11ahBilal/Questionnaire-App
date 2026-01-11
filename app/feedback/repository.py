from app.extensions import db
from app.models.answer import Answer
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError

class AnswerRepository:

    @staticmethod
    def save_bulk_answers(answers_data):
        
        try:
            for data in answers_data:
                new_answer = Answer(**data) 
                db.session.add(new_answer)

            db.session.commit()
            logger.debug(f"Database COMMIT success: {len(answers_data)} answers saved.")
            return True

        except SQLAlchemyError as e:
            db.session.rollback()
            
            logger.critical(f"Database ROLLBACK: bulk_save_answers failed | error={str(e)}")
            
            raise e