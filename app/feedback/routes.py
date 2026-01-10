from flask import render_template
from flask_login import login_required, current_user
from . import feedback_bp

@feedback_bp.route('/')
@login_required
def index():
    return render_template('feedback/index.html', user=current_user)