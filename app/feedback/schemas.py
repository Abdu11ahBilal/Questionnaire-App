from pydantic import BaseModel, field_validator
from typing import Dict
from .questions import QUESTIONS

VALID_QUESTION_IDS = {q['id'] for q in QUESTIONS}

class FeedbackPageSchema(BaseModel):

    answers: Dict[int, str]

    @field_validator('answers')
    @classmethod
    def validate_content(cls, v: Dict[int, str]):
        if not v:
            raise ValueError("At least one answer is required.")
            
        for q_id, val in v.items():
            
            if q_id not in VALID_QUESTION_IDS:
                raise ValueError(f"Question ID {q_id} is not part of this survey.")
            

            if not val.strip():
                raise ValueError(f"Answer for question {q_id} cannot be empty.")
        
        return v