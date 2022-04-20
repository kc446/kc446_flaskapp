"""A simple Flask web app."""
import os

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_wtf.csrf import CSRFProtect

import flask_login
from flaskApp.auth import auth
from flaskApp.cli import create_database, create_log_folder
from flaskApp.context_processors import utility_text_processors
from flaskApp.db import db
from flaskApp.db.models import User
from flaskApp.error_handlers import error_handlers
from flaskApp.map import map
from flaskApp.simple_pages import simple_pages
from flaskApp.songs import songs

login_manager = flask_login.LoginManager()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    #trying something here to see if it's the port for some reason
    if __name__ == "__main__":
        port = int(os.environ.get("PORT", 5000))
        app.run(host='0.0.0.0', port=port)

    if app.config["ENV"] == "production":
        app.config.from_object("flaskApp.config.ProductionConfig")
    elif app.config["ENV"] == "development":
        app.config.from_object("flaskApp.config.DevelopmentConfig")
    elif app.config["ENV"] == "testing":
        app.config.from_object("flaskApp.config.TestingConfig")

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf = CSRFProtect(app)
    csrf.exempt(auth)
    bootstrap = Bootstrap5(app)

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
    app.register_blueprint(error_handlers)
    app.register_blueprint(songs)
    app.register_blueprint(map)

    app.add_url_rule("/", endpoint="index")
    app.context_processor(utility_text_processors)

    app.cli.add_command(create_database)
    app.cli.add_command(create_log_folder)
    db.init_app(app)

    return app

@login_manager.user_loader
def user_loader(user_id):
    try:
        print(User.get_id()) #prints the user id table
        user.get_id() #gets the user id
        return User.query.get(int(user_id))
    except:
        return None
