"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name

import os

import pytest

from flaskApp import create_app, User
from flaskApp.db import db


@pytest.fixture()
def application():
    """This makes the app"""
    os.environ['FLASK_ENV'] = 'development'
    application = create_app()
    application.config.update(ENV="development")

    with application.app_context():
        db.create_all()
        yield application
        db.session.remove()
        # drops the database tables after the test runs
        # db.drop_all()

@pytest.fixture()
def add_user(application):
    with application.app_context():
        #new record
        user = User('test@email.com', 'pwtest')
        db.session.add(user)
        #db.session.commit()

@pytest.fixture()
def client(application):
    """This makes the http client"""
    return application.test_client()


@pytest.fixture()
def runner(application):
    """This makes the task runner"""
    return application.test_cli_runner()
