def test_submit_review_session_success(
    client,
    mock_valid_token,
    monkeypatch
):
    def fake_process_review_session(
        user_id,
        review_results,
        timezone_name
    ):
        return [
            {
                "status": "updated",
                "card_id": "Hund"
            },
            {
                "status": "updated",
                "card_id": "Katze"
            }
        ]

    monkeypatch.setattr(
        "app.api.reviews.process_review_session",
        fake_process_review_session
    )

    response = client.post(
        "/api/review/session",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "timezone": "Europe/Dublin",
            "review_results": [
                {
                    "card_id": "Hund",
                    "decision": "OK",
                    "again_count": 0
                },
                {
                    "card_id": "Katze",
                    "decision": "EASY",
                    "again_count": 1
                }
            ]
        }
    )

    assert response.status_code == 200

    assert response.get_json() == {
        "results": [
            {
                "status": "updated",
                "card_id": "Hund"
            },
            {
                "status": "updated",
                "card_id": "Katze"
            }
        ]
    }



def test_submit_review_session_empty_body(
    client,
    mock_valid_token
):
    response = client.post(
        "/api/review/session",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={}
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Request body is required"
    }


def test_submit_review_session_missing_timezone(
    client,
    mock_valid_token
):
    response = client.post(
        "/api/review/session",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "review_results": [
                {
                    "card_id": "Hund",
                    "decision": "OK"
                }
            ]
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Timezone is required"
    }


def test_submit_review_session_reviews_not_list(
    client,
    mock_valid_token
):
    response = client.post(
        "/api/review/session",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "timezone": "Europe/Dublin",
            "review_results": {
                "card_id": "Hund"
            }
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "review_results must be a list"
    }


def test_submit_review_session_empty_reviews(
    client,
    mock_valid_token
):
    response = client.post(
        "/api/review/session",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "timezone": "Europe/Dublin",
            "review_results": []
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "review_results must not be empty"
    }


def test_submit_review_session_review_item_not_object(
    client,
    mock_valid_token
):
    response = client.post(
        "/api/review/session",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "timezone": "Europe/Dublin",
            "review_results": [
                "Hund"
            ]
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Each review result must be an object"
    }


def test_submit_review_session_missing_card_id(
    client,
    mock_valid_token
):
    response = client.post(
        "/api/review/session",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "timezone": "Europe/Dublin",
            "review_results": [
                {
                    "decision": "OK",
                    "again_count": 0
                }
            ]
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Each review must contain a card_id"
    }


def test_submit_review_session_missing_decision(
    client,
    mock_valid_token
):
    response = client.post(
        "/api/review/session",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "timezone": "Europe/Dublin",
            "review_results": [
                {
                    "card_id": "Hund",
                    "again_count": 0
                }
            ]
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Each review result must contain decision"
    }


def test_submit_review_session_invalid_decision(
    client,
    mock_valid_token
):
    response = client.post(
        "/api/review/session",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "timezone": "Europe/Dublin",
            "review_results": [
                {
                    "card_id": "Hund",
                    "decision": "MAYBE",
                    "again_count": 0
                }
            ]
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "Decision must be OK or EASY"
    }


def test_submit_review_session_negative_again_count(
    client,
    mock_valid_token
):
    response = client.post(
        "/api/review/session",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "timezone": "Europe/Dublin",
            "review_results": [
                {
                    "card_id": "Hund",
                    "decision": "OK",
                    "again_count": -1
                }
            ]
        }
    )

    assert response.status_code == 400
    assert response.get_json() == {
        "error": "again_count must be a non-negative integer"
    }

#Authentication:
def test_submit_review_session_missing_token(client):
    response = client.post(
        "/api/review/session",
        json={
            "timezone": "Europe/Dublin",
            "review_results": [
                {
                    "card_id": "Hund",
                    "decision": "OK",
                    "again_count": 0
                }
            ]
        }
    )

    assert response.status_code == 401

def test_submit_review_session_passes_correct_data_to_service(
    client,
    mock_valid_token,
    monkeypatch
):
    received = {}

    def fake_process_review_session(
        user_id,
        review_results,
        timezone_name
    ):
        received["user_id"] = user_id
        received["review_results"] = review_results
        received["timezone_name"] = timezone_name

        return []

    monkeypatch.setattr(
        "app.api.reviews.process_review_session",
        fake_process_review_session
    )

    review_results = [
        {
            "card_id": "Hund",
            "decision": "OK",
            "again_count": 0
        }
    ]

    response = client.post(
        "/api/review/session",
        headers={
            "Authorization": "Bearer fake_token"
        },
        json={
            "timezone": "Europe/Dublin",
            "review_results": review_results
        }
    )

    assert response.status_code == 200

    assert received == {
        "user_id": mock_valid_token,
        "review_results": review_results,
        "timezone_name": "Europe/Dublin"
    }

