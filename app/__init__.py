from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # import the authentication blueprint and register it on the app
    from .user import user_blueprint
    from .word import word
    from .auth import auth_blueprint
    from .pos import pos_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(word)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(pos_blueprint)

    return app


