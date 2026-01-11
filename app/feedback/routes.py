import uuid
from flask import render_template, request, redirect, url_for, session, flash
from flask_login import login_required, current_user
from loguru import logger
from . import feedback_bp
from .questions import QUESTIONS
from .repository import AnswerRepository

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
    
    answers = {}
    
    for q in page_questions:
        
        val = request.form.get(str(q['id']))
        
        if not val:
            flash(f"Question {q['id']} is required!", "danger")
            return redirect(url_for('feedback.page_one'))
        
        answers[q['id']] = val

    if 'feedback_answers' not in session:
        session['feedback_answers'] = {}
    
    session_data = session.get('feedback_answers', {})
    session_data.update(answers)
    session['feedback_answers'] = session_data
    
    return redirect(url_for('feedback.page_two')) 

@feedback_bp.route('/page/2', methods=['GET', 'POST'])
@login_required 
def page_two():

    if 'feedback_answers' not in session:
        flash("Please complete the first page first.", "warning")
        return redirect(url_for('feedback.page_one'))

    page_questions = QUESTIONS[10:20]

    if request.method == 'GET':
        return render_template('feedback/page2.html', questions=page_questions)


    new_answers = {}
    for q in page_questions:
        val = request.form.get(str(q['id']))
        if not val:
            flash(f"Question {q['id']} is required!", "danger")
            return redirect(url_for('feedback.page_two'))
        new_answers[q['id']] = val

    session_data = session.get('feedback_answers', {})
    session_data.update(new_answers)
    session['feedback_answers'] = session_data

    return redirect(url_for('feedback.submit'))


@feedback_bp.route('/submit', methods=['POST', 'GET'])
@login_required
def submit():

    answers_dict = session.get('feedback_answers')
    if not answers_dict or len(answers_dict) < 20:
        flash("Incomplete submission. Please start over.", "danger")
        return redirect(url_for('feedback.page_one'))

    submission_id = str(uuid.uuid4())

    formatted_answers = []
    for q_id, val in answers_dict.items():
        formatted_answers.append({
            "user_id": current_user.id,
            "submission_id": submission_id,
            "question_id": int(q_id),
            "answer_value": val
        })

    try:
        AnswerRepository.save_bulk_answers(formatted_answers)
        
        session.pop('feedback_answers', None)
        logger.info(f"User {current_user.username} submitted feedback {submission_id}")
        
        return redirect(url_for('feedback.complete'))

    except Exception as e:
        logger.error(f"Submission failed for {current_user.username}: {e}")
        flash("A database error occurred. Your answers were not saved.", "danger")
        return redirect(url_for('feedback.page_two'))

@feedback_bp.route('/complete')
@login_required 
def complete():
    return render_template('feedback/complete.html')