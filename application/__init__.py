from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    """
        Init main application
    """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    db.init_app(app)

    with app.app_context():
        # import routes
        from .sentences import sentences
        db.create_all()

        # registering bps
        app.register_blueprint(sentences.sentences_bp)

        return app