
"""
    We do not need to define monkeypatch like we did with the client,
    as pythest already has built-in monkeypatch fixture,
     we can just add it as a parameter to the test function.

"""
from google.api_core.gapic_v1 import requests

import os
import requests

from dotenv import load_dotenv

load_dotenv(".env.test")

def test_auth_required_accepts_valid_token(client, monkeypatch):
    def fake_verify_id_token(token):
        return {"uid": "test_user_hehe"}

    monkeypatch.setattr(
        "app.auth.decorators.auth.verify_id_token",
        fake_verify_id_token
    )

    response = client.get(
        "/api/protected",
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 200
    assert response.get_json() == {"message": "Authenticated succesfully",
    "uid": "test_user_hehe"}
    print(response.get_json())

def get_token(email, password, api_key):
    url = (
        "https://identitytoolkit.googleapis.com/"
        f"v1/accounts:signInWithPassword?key={api_key}"#here we need to get the info from .env.test
    )

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    response = requests.post(url, json=payload)
    response.raise_for_status()  # Raise an exception for HTTP errors

    return response.json()["idToken"]





"""
def test_auth_required_real_token(client):
    email = os.getenv("FIREBASE_TEST_EMAIL")
    

    token = get_token()
    response = client.get(
        "/api/protected",
        headers={"Authorization": token}
    )
"""