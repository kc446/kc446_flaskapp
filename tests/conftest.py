"""This makes the test configuration setup"""
# pylint: disable=redefined-outer-name
import pytest

from flaskApp import create_app


@pytest.fixture()
def app():
    """This makes the app"""
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)