import click
from flask.cli import with_appcontext
from flaskApp.db import db


@click.command(name='create-db')
@with_appcontext
def create_database():
    db.create_all()
