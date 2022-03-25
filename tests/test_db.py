import sqlite3

import pytest


# it's definitely something with the db and how we switched it to SQLAlchemy but i guess i'll figure it out over the weekend
def test_get_close_db(app):
    with app.app_context():
        db = app.db #db(app)
        assert db is app.db #db(app)

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute("SELECT 1")

    assert "closed" in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder:
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr("flaskApp.db.init_db", fake_init_db())
    result = runner.invoke(args=["init-db"])
    assert "Initialized" in result.output
    assert Recorder.called
