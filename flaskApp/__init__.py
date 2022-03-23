"""A simple Flask web app."""
from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect

import os
from flaskApp import db, auth, blog, simple_pages
from flaskApp.context_processors import utility_text_processors
from flaskApp.simple_pages import simple_pages
from flaskApp.exceptions import http_exceptions
from flaskApp.db.models import User
from flaskApp.db import db
from flaskApp.auth import auth
from flaskApp.cli import create_database
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    current_user,
    logout_user,
    login_required,
)

login_manager = LoginManager()


def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

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
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

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

    app.add_url_rule("/", endpoint="index")
    app.context_processor(utility_text_processors)

    db_dir = "database/db.sqlite"
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.abspath(db_dir)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    app.cli.add_command(create_database)

    if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)
    return app


@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None


app = create_app()




