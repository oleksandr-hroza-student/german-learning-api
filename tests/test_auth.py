
"""
    We do not need to define monkeypatch like we did with the client,
    as pythest already has built-in monkeypatch fixture,
     we can just add it as a parameter to the test function.

"""
from google.api_core.gapic_v1 import requests


import os
import requests
import pytest

#helper method when I need to simulate a succesfull signin
def fake_verify_id_token(token):
    return {"uid": "test_user_hehe"}

def test_auth_required_accepts_valid_token(client, monkeypatch):

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
    #print(response.get_json())

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

@pytest.mark.integration
def test_auth_required_real_token(integration_client, user_credentials_for_test):
    creds = user_credentials_for_test

    token = get_token(creds["email"], creds["password"], creds["api_key"])
    response = integration_client.get(
        "/api/protected",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200



