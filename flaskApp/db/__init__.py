from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy

def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again."""
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If this request connected to the database, close the
    connection."""
    db = g.pop("db", None)

    if db is not None:
        db.close()

db = SQLAlchemy()

database = Blueprint('database', __name__,)


@database.cli.command('create')
def init_db():
    db.create_all()
