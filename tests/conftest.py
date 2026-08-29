#In this file we will create fixtures that we will later re-use for testing

import os
import pytest

from unittest.mock import MagicMock

from app import create_app

from dotenv import load_dotenv
load_dotenv(".env.test")

@pytest.fixture
def app():
    app = create_app()
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def user_credentials_for_test():
    email = os.getenv("TEST_USER_EMAIL")
    password = os.getenv("TEST_USER_PASSWORD")
    api_key = os.getenv("FIREBASE_WEB_API_KEY")

    assert email is not None, "TEST_USER_EMAIL not loaded"
    assert password is not None, "TEST_USER_PASSWORD not loaded"
    assert api_key is not None, "FIREBASE_WEB_API_KEY not loaded"

    return {
            "email": email,
            "password": password,
            "api_key": api_key
        }

@pytest.fixture
def mock_valid_token(monkeypatch):
    user_id = "test_user_hehe"
    def fake_verify_id_token(token):
        return {"uid": user_id}

    monkeypatch.setattr(
        "app.auth.decorators.auth.verify_id_token",
        fake_verify_id_token
    )

    return user_id

@pytest.fixture
def fake_db(monkeypatch):
    db = MagicMock()

    monkeypatch.setattr(
        "app.api.me.get_db",
        lambda: db
    )

    return db
