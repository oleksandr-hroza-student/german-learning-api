# POST /api/flashcards

#The correct behaviour with valid input
def test_create_flashcards_route_success(
    client,
    mock_valid_token,
    monkeypatch
):
    def fake_create_flashcards_from_text(user_id, text):
        return (
            [
                {
                    "status": "created",
                    "word": "Katze",
                    "gender": "f"
                }
            ],
            [
                {
                    "status": "already_exists",
                    "word": "Hund"
                }
            ]
        )

    monkeypatch.setattr(
        "app.api.flashcards.create_flashcards_from_text",
        fake_create_flashcards_from_text
    )

    response = client.post(
        "/api/flashcards",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "text": "Hund Katze"
        }
    )

    assert response.status_code == 201

    assert response.get_json() == {
        "created": [
            {
                "status": "created",
                "word": "Katze",
                "gender": "f"
            }
        ],
        "skipped": [
            {
                "status": "already_exists",
                "word": "Hund"
            }
        ]
    }

def test_create_flashcards_route_success(
    client,
    mock_valid_token,
    monkeypatch
):
    def fake_create_flashcards_from_text(user_id, text):
        return (
            [
                {
                    "status": "created",
                    "word": "Katze",
                    "gender": "f"
                }
            ],
            [
                {
                    "status": "already_exists",
                    "word": "Hund"
                }
            ]
        )

    monkeypatch.setattr(
        "app.api.flashcards.create_flashcards_from_text",
        fake_create_flashcards_from_text
    )

    response = client.post(
        "/api/flashcards",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "text": "Hund Katze"
        }
    )

    assert response.status_code == 201

    assert response.get_json() == {
        "created": [
            {
                "status": "created",
                "word": "Katze",
                "gender": "f"
            }
        ],
        "skipped": [
            {
                "status": "already_exists",
                "word": "Hund"
            }
        ]
    }


# Route passes correct user ID and text to service
def test_create_flashcards_route_passes_correct_data_to_service(
    client,
    mock_valid_token,
    monkeypatch
):
    received = {}

    def fake_create_flashcards_from_text(user_id, text):
        received["user_id"] = user_id
        received["text"] = text

        return (
            [],
            []
        )

    monkeypatch.setattr(
        "app.api.flashcards.create_flashcards_from_text",
        fake_create_flashcards_from_text
    )

    response = client.post(
        "/api/flashcards",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "text": "  Hund Katze  "
        }
    )

    assert response.status_code == 201

    assert received == {
        "user_id": mock_valid_token,
        "text": "Hund Katze"
    }