from unittest.mock import MagicMock
#from test_auth import fake_verify_id_token
def test_get_me_existing_profile(client, monkeypatch, mock_valid_token):
    #Replaces the actual function (from firebase_admin import auth; auth.veryfi_id_token)
    #with a fake one, that just returns a user id in this case

    """
    here we are creating a fake firestore snapshot:
    (fake version of DocumentSnapshot), we can continue testing as though Firestore returned a real document;
    "Create an object that can pretend to have whatever attibutes/methods I need"
    """

    fake_snapshot = MagicMock()
    #(The exists attribute is set to True)
    fake_snapshot.exists = True
    #The to_dict method would behave as follows:
    fake_snapshot.to_dict.return_value = {
        "username" : "test_user_username",
        "streak" : 5
    }


    fake_db = MagicMock()
    fake_db.collection.return_value.document.return_value.get.return_value = fake_snapshot

    monkeypatch.setattr(
        "app.api.me.get_db",
        lambda: fake_db
    )
    """
    fake_db.collection() - returns a fake collection
    fake_db.collection.document() - returns a fake document
    fake_db.collection.document.get() - returns a fake snapshot (that we have defined earlier)
    """


    response = client.get("/api/me", headers={"Authorization": "Bearer fake_token"})

    assert response.status_code == 200
    assert response.get_json() == {
        "username": "test_user_username",
        "streak": 5
    }

def test_get_me_not_existing_profile(client, monkeypatch, mock_valid_token):
    #Replaces the actual function (from firebase_admin import auth; auth.veryfi_id_token)
    #with a fake one, that just returns a user id in this case
    expected_uid = mock_valid_token


    """
    here we are creating a fake firestore snapshot:
    (fake version of DocumentSnapshot), we can continue testing as though Firestore returned a real document;
    "Create an object that can pretend to have whatever attibutes/methods I need"
    """

    fake_snapshot = MagicMock()
    #(The exists attribute is set to True)
    fake_snapshot.exists = False



    fake_db = MagicMock()
    fake_db.collection.return_value.document.return_value.get.return_value = fake_snapshot

    monkeypatch.setattr(
        "app.api.me.get_db",
        lambda: fake_db
    )
    """
    fake_db.collection() - returns a fake collection
    fake_db.collection.document() - returns a fake document
    fake_db.collection.document.get() - returns a fake snapshot (that we have defined earlier)
    """


    response = client.get("/api/me", headers={"Authorization": "Bearer fake_token"})

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "User profile not found"
    }

def test_get_me_without_token(client):
    response = client.get("/api/me")

    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Missing or invalid Authorisation header"
    }


def test_get_me_invalid_token(client, monkeypatch):
    def fake_invalid_token(token):
        raise Exception("Token is invalid")

    monkeypatch.setattr(
        "app.auth.decorators.auth.verify_id_token",
        fake_invalid_token
    )

    response = client.get(
        "/api/me",
        headers={"Authorization": "Bearer bad_token"}
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid token"



def test_get_me_uses_authenticated_user_uid(client, monkeypatch, mock_valid_token):
    expected_uid = mock_valid_token

    fake_snapshot = MagicMock()
    fake_snapshot.exists = True
    fake_snapshot.to_dict.return_value = {
        "username": "test_user_username",
        "streak": 5
    }

    fake_db = MagicMock()
    fake_db.collection.return_value.document.return_value.get.return_value = fake_snapshot

    monkeypatch.setattr(
        "app.api.me.get_db",
        lambda: fake_db
    )

    response = client.get(
        "/api/me",
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 200

    fake_db.collection.assert_called_once_with("users")

    fake_db.collection.return_value.document.assert_called_once_with(
        expected_uid
    )