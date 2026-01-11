import uuid
from flask import render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from loguru import logger
from pydantic import ValidationError

from . import feedback_bp
from .questions import QUESTIONS
from .repository import AnswerRepository
from .schemas import FeedbackPageSchema 

@feedback_bp.route('/')
@login_required
def index():
    return render_template('feedback/index.html', user=current_user)

@feedback_bp.route('/page/1', methods=['GET', 'POST'])
@login_required 
def page_one():
    page_questions = QUESTIONS[0:10]

    if request.method == 'GET':
        return render_template('feedback/page1.html', questions=page_questions)
    
    try:
        # Pydantic handles type conversion and required checks
        form_data = FeedbackPageSchema(answers=request.form.to_dict()) # type: ignore
    except ValidationError as e:
        logger.warning(f"User {current_user.id} - Page 1 Validation Error: {e.errors()}")
        flash("Please answer all questions on this page.", "danger")
        return redirect(url_for('feedback.page_one'))


    session_data = session.get('feedback_answers', {})
    session_data.update(form_data.answers)
    session['feedback_answers'] = session_data
    
    logger.info(f"User {current_user.id} completed Page 1")
    return redirect(url_for('feedback.page_two'))

@feedback_bp.route('/page/2', methods=['GET', 'POST'])
@login_required 
def page_two():
    
    if 'feedback_answers' not in session:
        logger.warning(f"User {current_user.id} tried to bypass Page 1.")
        flash("Please complete the first page first.", "warning")
        return redirect(url_for('feedback.page_one'))

    page_questions = QUESTIONS[10:20]

    if request.method == 'GET':
        return render_template('feedback/page2.html', questions=page_questions)

    try:
        form_data = FeedbackPageSchema(answers=request.form.to_dict()) # type: ignore
    except ValidationError as e:
        logger.warning(f"User {current_user.id} - Page 2 Validation Error: {e.errors()}")
        flash("Please answer all questions on this page.", "danger")
        return redirect(url_for('feedback.page_two'))

    session_data = session.get('feedback_answers', {})
    session_data.update(form_data.answers)
    session['feedback_answers'] = session_data

    logger.info(f"User {current_user.id} completed Page 2")
    return redirect(url_for('feedback.submit'))

@feedback_bp.route('/submit', methods=['POST', 'GET'])
@login_required
def submit():
    answers_dict = session.get('feedback_answers')
    
    if not answers_dict or len(answers_dict) < 20:
        logger.error(f"User {current_user.id} attempted submission with incomplete data.")
        flash("Incomplete submission. Please start over.", "danger")
        return redirect(url_for('feedback.page_one'))

    logger.info(f"User {current_user.id} initiating final submission.")
    submission_id = str(uuid.uuid4())

    formatted_answers = [
        {
            "user_id": current_user.id,
            "submission_id": submission_id,
            "question_id": q_id,  
            "answer_value": val
        }
        for q_id, val in answers_dict.items()
    ]

    try:
        AnswerRepository.save_bulk_answers(formatted_answers)
        
        session.pop('feedback_answers', None)
        logger.info(f"Submission SUCCESS: user_id={current_user.id} | sub_id={submission_id}")
        
        return redirect(url_for('feedback.complete'))

    except Exception as e:
        logger.critical(f"DATABASE CRASH during submission: {e}")
        flash("We couldn't save your answers due to a temporary server issue. Please try clicking submit again.", "danger")
        return redirect(url_for('feedback.page_two'))

@feedback_bp.route('/complete')
@login_required 
def complete():
    return render_template('feedback/complete.html')