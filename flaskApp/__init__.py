"""A simple Flask web app."""
import os

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap5
from flask_login import (
    LoginManager,
)
from flask_wtf.csrf import CSRFProtect

from flaskApp import db, auth, simple_pages
from flaskApp.auth import auth
from flaskApp.cli import create_database
from flaskApp.context_processors import utility_text_processors
from flaskApp.db import db
from flaskApp.db.models import User
from flaskApp.simple_pages import simple_pages

login_manager = LoginManager()

def page_not_found(e):
    return render_template("404.html"), 404

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    app.secret_key = 'This is an INSECURE secret!! DO NOT use this in production!!'
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf = CSRFProtect(app)
    bootstrap = Bootstrap5(app)

    app.config.from_mapping(
        # a default secret that should be overridden by instance config
        SECRET_KEY="dev",
        # store the database in the instance folder
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    # register the database commands
    db.init_app(app)
    # apply the blueprints to the app
    app.register_blueprint(auth)
    app.register_blueprint(simple_pages)
    app.context_processor(utility_text_processors)
    app.register_error_handler(404, page_not_found)

    app.config['BOOTSTRAP_BOOTSWATCH_THEME'] = 'Simplex'

    # app.add_url_rule("/", endpoint="index")

    db_dir = "database/db.sqlite"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(db_dir)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.cli.add_command(create_database)

    return app

@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None
