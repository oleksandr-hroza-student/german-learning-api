import requests
import os
from dotenv import load_dotenv
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
env_path = project_root / ".env.test"

load_dotenv(env_path)

email = os.getenv("TEST_USER_EMAIL")
password = os.getenv("TEST_USER_PASSWORD")
api_key = os.getenv("FIREBASE_WEB_API_KEY")

print("EMAIL FOUND:", email is not None)
print("PASSWORD FOUND:", password is not None)
print("API KEY FOUND:", api_key is not None)

url = (
    "https://identitytoolkit.googleapis.com/"
    f"v1/accounts:signInWithPassword?key={api_key}"
)

payload = {
    "email": email,
    "password": password,
    "returnSecureToken": True
}

response = requests.post(url, json=payload)
response.raise_for_status()

token = response.json()["idToken"]

print("Got token")

response = requests.post(
    "http://127.0.0.1:5000/api/me",
    headers={
        "Authorization": f"Bearer {token}"
    },
    json={
            "username": "The goat"
        }
)

response = requests.patch(
    "http://127.0.0.1:5000/api/me",
    headers={
        "Authorization": f"Bearer {token}"
    },
    json={
        "username": "updated_username"
    }
)

print(response.status_code)
print(response.json())

response = requests.get(
    "http://127.0.0.1:5000/api/me",
    headers={
        "Authorization": f"Bearer {token}"
    }
)

print(response.status_code)
print(response.json())