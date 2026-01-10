from app.extensions import db

class Answer(db.Model):
    __tablename__ = 'answers'

    id = db.Column(db.Integer, primary_key=True)

   
    submission_id = db.Column(db.String(36), nullable=False)

    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    question_id = db.Column(db.Integer, nullable=False)

    answer_value = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<Answer User:{self.user_id} Submission:{self.submission_id}>'