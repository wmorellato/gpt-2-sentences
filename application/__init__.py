import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .database import Session, init_db

# importing gpt stuff
from .gpt.manager import Manager

def shutdown_session(exception=None):
    Session.remove()


def create_app():
    """
        Init main application
    """
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.DevConfig')

    with app.app_context():        
        # import routes
        from .sentences import sentences

        # create db
        init_db()
        app.db_session = Session()
        app.teardown_appcontext(shutdown_session)
        app.base_path = os.path.dirname(app.instance_path)
        manager = Manager(app)

        # registering bps
        app.register_blueprint(sentences.sentences_bp, url_prefix='/%s' % app.config['API_VERSION'])

        return app