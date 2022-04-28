"""A simple Flask web app."""

from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_cors import CORS
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

import flask_login
from flaskApp.auth import auth
from flaskApp.cli import create_database
from flaskApp.context_processors import utility_text_processors
from flaskApp.db import database
from flaskApp.db import db
from flaskApp.db.models import User
from flaskApp.error_handlers import error_handlers
from flaskApp.logging_config import log_con
from flaskApp.map import map
from flaskApp.simple_pages import simple_pages
from flaskApp.songs import songs

mail = Mail()
login_manager = flask_login.LoginManager()

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)
    #trying something here to see if it's the port for some reason
    #if __name__ == "__main__":
        #port = int(os.environ.get("PORT", 5000))
        #app.run(host='0.0.0.0', port=port)

    if app.config["ENV"] == "production":
        app.config.from_object("flaskApp.config.ProductionConfig")
    elif app.config["ENV"] == "development":
        app.config.from_object("flaskApp.config.DevelopmentConfig")
    elif app.config["ENV"] == "testing":
        app.config.from_object("flaskApp.config.TestingConfig")
    app.mail = Mail(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    csrf = CSRFProtect(app)
    csrf.exempt(auth)
    bootstrap = Bootstrap5(app)

    # apply the blueprints to the app
    app.register_blueprint(auth)
    app.register_blueprint(database)
    app.register_blueprint(simple_pages)

    # these load functionality with out a web interface
    app.register_blueprint(log_con)
    app.register_blueprint(error_handlers)

    app.register_blueprint(songs)
    app.register_blueprint(map)

    app.context_processor(utility_text_processors)

    # add command function to cli commands
    app.cli.add_command(create_database)
    db.init_app(app)

    api_v1_cors_config = {"methods": ["OPTIONS", "GET", "POST"]}
    CORS(app, resources={"/api/*": api_v1_cors_config})

    # Run once at startup
    return app

@login_manager.user_loader
def user_loader(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None
