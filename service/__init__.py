from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os

# Set the directory of this file to the current directory.
dir_name = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_name)


def create_app():
    from service.config import Config
    app = Flask(__name__)
    app.config.from_object(Config)
    return app

def create_db():
    db = SQLAlchemy(app)
    return db

def register_routes():
    from service.blueprints.user import user_blueprint
    from service.blueprints.message import message_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(message_blueprint)


app = create_app()
db = create_db()

register_routes()

@app.before_first_request
def before_first_request():
    eng = db.get_engine()
    if not eng.table_names():
        from service.models import init_db
        init_db()
