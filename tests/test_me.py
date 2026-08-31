from unittest.mock import MagicMock
#from test_auth import fake_verify_id_token

#GET TESTS:

#valid token + profile exists
def test_get_me_existing_profile(client, mock_valid_token, fake_db):
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


    #fake_db = MagicMock()
    fake_db.collection.return_value.document.return_value.get.return_value = fake_snapshot
    """
    Not needed, as made a fake_db fixture
    monkeypatch.setattr(
        "app.api.me.get_db",
        lambda: fake_db
    )
    """
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

#valid token + profile missing
def test_get_me_not_existing_profile(client, mock_valid_token, fake_db):
    #Replaces the actual function (from firebase_admin import auth; auth.veryfi_id_token)
    #with a fake one, that just returns a user id in this case


    """
    here we are creating a fake firestore snapshot:
    (fake version of DocumentSnapshot), we can continue testing as though Firestore returned a real document;
    "Create an object that can pretend to have whatever attibutes/methods I need"
    """

    fake_snapshot = MagicMock()
    #(The exists attribute is set to True)
    fake_snapshot.exists = False



    #fake_db = MagicMock()
    fake_db.collection.return_value.document.return_value.get.return_value = fake_snapshot
    """
    monkeypatch.setattr(
        "app.api.me.get_db",
        lambda: fake_db
    )
    """
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

#no token
def test_get_me_without_token(client):
    response = client.get("/api/me")

    assert response.status_code == 401
    assert response.get_json() == {
        "error": "Missing or invalid Authorisation header"
    }


#invalid token
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



def test_get_me_uses_authenticated_user_uid(client, mock_valid_token, fake_db):
    expected_uid = mock_valid_token

    fake_snapshot = MagicMock()
    fake_snapshot.exists = True
    fake_snapshot.to_dict.return_value = {
        "username": "test_user_username",
        "streak": 5
    }

    #fake_db = MagicMock()
    fake_db.collection.return_value.document.return_value.get.return_value = fake_snapshot

    """
    Not needed, as we have done this bit in the fixture already
    monkeypatch.setattr(
        "app.api.me.get_db",
        lambda: fake_db
    )
    """
    response = client.get(
        "/api/me",
        headers={"Authorization": "Bearer fake_token"}
    )

    assert response.status_code == 200

    fake_db.collection.assert_called_once_with("users")

    fake_db.collection.return_value.document.assert_called_once_with(
        expected_uid
    )


#POST TESTS:

#Valid token + profile does not exist


def test_post_me_creates_new_profile(client, mock_valid_token, fake_db):
    fake_snapshot = MagicMock()
    fake_snapshot.exists = False

    fake_db.collection.return_value.document.return_value.get.return_value = fake_snapshot

    response = client.post(
        "/api/me",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "username": "test_username"
        }
    )

    assert response.status_code == 201
    assert response.get_json() == {
        "message": "User profile created"
    }

#Check that when creating the profile it actually wrote the correct data:
#(Instead of "streak" : 67, "username" : 676767)

def test_post_me_writes_correct_profile_data(client, mock_valid_token, fake_db):
    fake_snapshot = MagicMock()
    fake_snapshot.exists = False

    fake_document = fake_db.collection.return_value.document.return_value
    fake_document.get.return_value = fake_snapshot

    response = client.post(
        "/api/me",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "username": "alex"
        }
    )

    assert response.status_code == 201

    fake_document.set.assert_called_once_with({
        "streak": 0,
        "username": "alex"
    })

#Test user profile already exists:


def test_post_me_existing_profile_returns_409(client, mock_valid_token, fake_db):
    fake_snapshot = MagicMock()
    fake_snapshot.exists = True

    fake_db.collection.return_value.document.return_value.get.return_value = fake_snapshot

    response = client.post(
        "/api/me",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "username": "test_username"
        }
    )

    assert response.status_code == 409

    assert response.get_json() == {
        "error": "User profile already exists"
    }


#the function does not overrite the existing profile:

def test_post_me_existing_profile_does_not_overwrite_profile(client, mock_valid_token, fake_db):
    fake_snapshot = MagicMock()
    fake_snapshot.exists = True

    fake_document = fake_db.collection.return_value.document.return_value
    fake_document.get.return_value = fake_snapshot

    response = client.post(
        "/api/me",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "username": "hacker_username"
        }
    )

    assert response.status_code == 409

    fake_document.set.assert_not_called()

#Try post with no token:

def test_post_me_without_token_returns_401(client):
    response = client.post(
        "/api/me",
        json={
            "username": "alex"
        }
    )

    assert response.status_code == 401

    assert response.get_json() == {
        "error": "Missing or invalid Authorisation header"
    }


#Try invalid token:

def test_post_me_invalid_token_returns_401(client, monkeypatch):
    def fake_invalid_token(token):
        raise Exception("Invalid token")

    monkeypatch.setattr(
        "app.auth.decorators.auth.verify_id_token",
        fake_invalid_token
    )

    response = client.post(
        "/api/me",
        headers={
            "Authorization": "Bearer bad_token"
        },
        json={
            "username": "alex"
        }
    )

    assert response.status_code == 401

    assert response.get_json()["error"] == "Invalid token"


#Test that post uses the default value in case no username provided:

def test_post_me_empty_username_uses_default(client, mock_valid_token, fake_db):
    fake_snapshot = MagicMock()
    fake_snapshot.exists = False

    fake_document = fake_db.collection.return_value.document.return_value
    fake_document.get.return_value = fake_snapshot

    response = client.post(
        "/api/me",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "username": ""
        }
    )

    assert response.status_code == 201

    fake_document.set.assert_called_once_with({
        "streak": 0,
        "username": "temp_username"
    })


#TESTS FOR PATCH:


def test_patch_me_updates_username(
    client,
    mock_valid_token,
    fake_db
):
    fake_snapshot = MagicMock()
    fake_snapshot.exists = True

    fake_document = fake_db.collection.return_value.document.return_value
    fake_document.get.return_value = fake_snapshot

    response = client.patch(
        "/api/me",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "username": "new_username"
        }
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "message": "User profile updated"
    }

    fake_document.update.assert_called_once_with({
        "username": "new_username"
    })


def test_patch_me_profile_not_found(
    client,
    mock_valid_token,
    fake_db
):
    fake_snapshot = MagicMock()
    fake_snapshot.exists = False

    fake_document = fake_db.collection.return_value.document.return_value
    fake_document.get.return_value = fake_snapshot

    response = client.patch(
        "/api/me",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "username": "new_username"
        }
    )

    assert response.status_code == 404
    assert response.get_json() == {
        "error": "User profile not found"
    }

    fake_document.update.assert_not_called()


def test_patch_me_empty_username_returns_400(
    client,
    mock_valid_token,
    fake_db
):
    response = client.patch(
        "/api/me",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "username": ""
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Username is required"
    }

    fake_db.collection.assert_not_called()


def test_patch_me_missing_body_returns_400(
    client,
    mock_valid_token,
    fake_db
):
    response = client.patch(
        "/api/me",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={}
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "No data provided"
    }

    fake_db.collection.assert_not_called()


def test_patch_me_without_token_returns_401(
    client
):
    response = client.patch(
        "/api/me",
        json={
            "username": "new_username"
        }
    )

    assert response.status_code == 401


def test_patch_me_invalid_token_returns_401(
    client,
    monkeypatch
):
    def fake_invalid_token(token):
        raise Exception("Invalid token")

    monkeypatch.setattr(
        "app.auth.decorators.auth.verify_id_token",
        fake_invalid_token
    )

    response = client.patch(
        "/api/me",
        headers={
            "Authorization": "Bearer bad_token"
        },
        json={
            "username": "new_username"
        }
    )

    assert response.status_code == 401
    assert response.get_json()["error"] == "Invalid token"


def test_patch_me_uses_authenticated_user_uid(
    client,
    mock_valid_token,
    fake_db
):
    expected_uid = mock_valid_token

    fake_snapshot = MagicMock()
    fake_snapshot.exists = True

    fake_document = fake_db.collection.return_value.document.return_value
    fake_document.get.return_value = fake_snapshot

    response = client.patch(
        "/api/me",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "username": "new_username"
        }
    )

    assert response.status_code == 200

    fake_db.collection.assert_called_once_with("users")

    fake_db.collection.return_value.document.assert_called_once_with(
        expected_uid
    )


def test_patch_me_ignores_protected_fields(
    client,
    mock_valid_token,
    fake_db
):
    fake_snapshot = MagicMock()
    fake_snapshot.exists = True

    fake_document = fake_db.collection.return_value.document.return_value
    fake_document.get.return_value = fake_snapshot

    response = client.patch(
        "/api/me",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "username": "new_username",
            "streak": 999999
        }
    )

    assert response.status_code == 200

    fake_document.update.assert_called_once_with({
        "username": "new_username"
    })