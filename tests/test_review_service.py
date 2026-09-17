from datetime import datetime, timezone

from app.services.review_service import review_flashcard


def test_review_flashcard_success(monkeypatch):
    fake_card = {
        "word": "Hund",
        "gender": "m",
        "interval_days": 3
    }

    fake_review_result = {
        "interval_days": 7,
        "next_review_at": datetime(
            2026, 9, 23,
            0, 0,
            tzinfo=timezone.utc
        )
    }

    fake_update_result = {
        "status": "updated",
        "card_id": "Hund",
        "interval_days": 7,
        "next_review_at": fake_review_result["next_review_at"]
    }

    monkeypatch.setattr(
        "app.services.review_service.get_flashcard",
        lambda user_id, card_id: fake_card
    )

    monkeypatch.setattr(
        "app.services.review_service.process_review",
        lambda current_interval, decision, now, timezone_name:
            fake_review_result
    )

    monkeypatch.setattr(
        "app.services.review_service.update_flashcard_review",
        lambda user_id, card_id, interval_days, next_review_at:
            fake_update_result
    )

    result = review_flashcard(
        "test_user_123",
        "Hund",
        "OK",
        "Europe/Dublin"
    )

    assert result == fake_update_result


def test_review_flashcard_not_found(monkeypatch):
    monkeypatch.setattr(
        "app.services.review_service.get_flashcard",
        lambda user_id, card_id: None
    )

    result = review_flashcard(
        "test_user_123",
        "Hund",
        "OK",
        "Europe/Dublin"
    )

    assert result == {
        "status": "not_found",
        "card_id": "Hund"
    }

def test_review_flashcard_passes_current_interval_to_scheduler(monkeypatch):
    received = {}

    monkeypatch.setattr(
        "app.services.review_service.get_flashcard",
        lambda user_id, card_id: {
            "word": "Hund",
            "gender": "m",
            "interval_days": 14
        }
    )

    def fake_process_review(
        current_interval,
        decision,
        now,
        timezone_name
    ):
        received["current_interval"] = current_interval
        received["decision"] = decision
        received["timezone_name"] = timezone_name

        return {
            "interval_days": 28,
            "next_review_at": datetime(
                2026, 10, 1,
                0, 0,
                tzinfo=timezone.utc
            )
        }

    monkeypatch.setattr(
        "app.services.review_service.process_review",
        fake_process_review
    )

    monkeypatch.setattr(
        "app.services.review_service.update_flashcard_review",
        lambda user_id, card_id, interval_days, next_review_at: {
            "status": "updated"
        }
    )

    review_flashcard(
        "test_user_123",
        "Hund",
        "OK",
        "Europe/Dublin"
    )

    assert received["current_interval"] == 14
    assert received["decision"] == "OK"
    assert received["timezone_name"] == "Europe/Dublin"



def test_review_flashcard_defaults_missing_interval_to_zero(monkeypatch):
    received = {}

    monkeypatch.setattr(
        "app.services.review_service.get_flashcard",
        lambda user_id, card_id: {
            "word": "Hund",
            "gender": "m"
        }
    )

    def fake_process_review(
        current_interval,
        decision,
        now,
        timezone_name
    ):
        received["current_interval"] = current_interval

        return {
            "interval_days": 1,
            "next_review_at": datetime(
                2026, 9, 17,
                0, 0,
                tzinfo=timezone.utc
            )
        }

    monkeypatch.setattr(
        "app.services.review_service.process_review",
        fake_process_review
    )

    monkeypatch.setattr(
        "app.services.review_service.update_flashcard_review",
        lambda user_id, card_id, interval_days, next_review_at: {
            "status": "updated"
        }
    )

    review_flashcard(
        "test_user_123",
        "Hund",
        "OK",
        "Europe/Dublin"
    )

    assert received["current_interval"] == 0

