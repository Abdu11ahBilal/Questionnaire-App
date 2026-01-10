from flask import Flask
from .config import Config
from .extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' # type: ignore

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .feedback import feedback_bp
    app.register_blueprint(feedback_bp)

    return app