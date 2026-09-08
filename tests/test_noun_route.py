"""
These tests are focused on the HTTP behaviour instead of
the service logic
"""

#Valid request with mocked service response
def test_process_nouns_valid_request(
    client,
    mock_valid_token,
    monkeypatch
):
    def fake_process_multiple_nouns(text):
        return [
            {
                "status": "found",
                "word": "Hund",
                "gender": "m"
            },
            {
                "status": "found",
                "word": "Katze",
                "gender": "f"
            }
        ]

    monkeypatch.setattr(
        "app.api.nouns.noun_service.process_multiple_nouns",
        fake_process_multiple_nouns
    )

    response = client.post(
        "/api/nouns/process",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "text": "Hund Katze"
        }
    )

    assert response.status_code == 200
    assert response.get_json() == [
        {
            "status": "found",
            "word": "Hund",
            "gender": "m"
        },
        {
            "status": "found",
            "word": "Katze",
            "gender": "f"
        }
    ]

#Missing request body
def test_process_nouns_missing_body(
    client,
    mock_valid_token
):
    response = client.post(
        "/api/nouns/process",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={}
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Request body is required"
    }

#Text is empty in the request
def test_process_nouns_empty_text(
    client,
    mock_valid_token
):
    response = client.post(
        "/api/nouns/process",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "text": ""
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Text is required"
    }

#No token at all
def test_process_nouns_without_token(client):
    response = client.post(
        "/api/nouns/process",
        json={
            "text": "Hund Katze"
        }
    )

    assert response.status_code == 401


#invalid toke
def test_process_nouns_invalid_token(
    client,
    monkeypatch
):
    def fake_invalid_token(token):
        raise Exception("Invalid token")

    monkeypatch.setattr(
        "app.auth.decorators.auth.verify_id_token",
        fake_invalid_token
    )

    response = client.post(
        "/api/nouns/process",
        headers={
            "Authorization": "Bearer bad_token"
        },
        json={
            "text": "Hund Katze"
        }
    )

    assert response.status_code == 401

"""
request JSON -> route extracts text -> route passes that string -> service receives it
"""
def test_process_nouns_passes_text_to_service(
    client,
    mock_valid_token,
    monkeypatch
):
    received_text = {}

    def fake_process_multiple_nouns(text):
        received_text["value"] = text
        return []

    monkeypatch.setattr(
        "app.api.nouns.noun_service.process_multiple_nouns",
        fake_process_multiple_nouns
    )

    response = client.post(
        "/api/nouns/process",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "text": "Hund Katze"
        }
    )

    assert response.status_code == 200
    assert received_text["value"] == "Hund Katze"