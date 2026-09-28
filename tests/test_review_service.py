from datetime import datetime, timezone

from app.services.review_service import review_flashcard, process_review_session, get_due_cards_for_user

def test_process_review_session_can_return_mixed_results(monkeypatch):
    def fake_review_flashcard(
        user_id,
        card_id,
        decision,
        timezone_name,
        reset_interval=False
    ):
        if card_id == "Hund":
            return {
                "status": "not_due",
                "card_id": "Hund"
            }

        return {
            "status": "updated",
            "card_id": card_id
        }

    monkeypatch.setattr(
        "app.services.review_service.review_flashcard",
        fake_review_flashcard
    )

    reviews = [
        {
            "card_id": "Hund",
            "decision": "OK",
            "again_count": 0
        },
        {
            "card_id": "Katze",
            "decision": "EASY",
            "again_count": 0
        }
    ]

    result = process_review_session(
        "test_user_123",
        reviews,
        "Europe/Dublin"
    )

    assert result == [
        {
            "status": "not_due",
            "card_id": "Hund"
        },
        {
            "status": "updated",
            "card_id": "Katze"
        }
    ]


def test_review_flashcard_not_due_does_not_reschedule(monkeypatch):
    future_time = datetime(
        2099, 1, 1,
        0, 0,
        tzinfo=timezone.utc
    )

    monkeypatch.setattr(
        "app.services.review_service.get_flashcard",
        lambda user_id, card_id: {
            "interval_days": 7,
            "next_review_at": future_time
        }
    )

    def fake_process_review(*args, **kwargs):
        raise AssertionError(
            "process_review should not be called for a card that is not due"
        )

    def fake_update_flashcard_review(*args, **kwargs):
        raise AssertionError(
            "repository update should not happen for a card that is not due"
        )

    monkeypatch.setattr(
        "app.services.review_service.process_review",
        fake_process_review
    )

    monkeypatch.setattr(
        "app.services.review_service.update_flashcard_review",
        fake_update_flashcard_review
    )

    result = review_flashcard(
        "test_user_123",
        "Hund",
        "OK",
        "Europe/Dublin"
    )

    assert result["status"] == "not_due"

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

def test_review_flashcard_resets_interval_when_requested(monkeypatch):
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

        return {
            "interval_days": 1,
            "next_review_at": "fake_timestamp"
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
        "Europe/Dublin",
        reset_interval=True
    )

    assert received["current_interval"] == 0
    assert received["decision"] == "OK"


def test_review_flashcard_keeps_interval_when_not_reset(monkeypatch):
    received = {}

    monkeypatch.setattr(
        "app.services.review_service.get_flashcard",
        lambda user_id, card_id: {
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

        return {
            "interval_days": 28,
            "next_review_at": "fake_timestamp"
        }

    monkeypatch.setattr(
        "app.services.review_service.process_review",
        fake_process_review
    )

    monkeypatch.setattr(
        "app.services.review_service.update_flashcard_review",
        lambda *args: {
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

    def test_process_review_session_processes_all_reviews(monkeypatch):
        calls = []

        def fake_review_flashcard(
                user_id,
                card_id,
                decision,
                timezone_name,
                reset_interval=False
        ):
            calls.append({
                "user_id": user_id,
                "card_id": card_id,
                "decision": decision,
                "timezone_name": timezone_name,
                "reset_interval": reset_interval
            })

            return {
                "status": "updated",
                "card_id": card_id
            }

        monkeypatch.setattr(
            "app.services.review_service.review_flashcard",
            fake_review_flashcard
        )

        reviews = [
            {
                "card_id": "Hund",
                "decision": "OK",
                "again_count": 0
            },
            {
                "card_id": "Katze",
                "decision": "EASY",
                "again_count": 0
            }
        ]

        result = process_review_session(
            "test_user_123",
            reviews,
            "Europe/Dublin"
        )

        assert len(calls) == 2

        assert calls[0] == {
            "user_id": "test_user_123",
            "card_id": "Hund",
            "decision": "OK",
            "timezone_name": "Europe/Dublin",
            "reset_interval": False
        }

        assert calls[1] == {
            "user_id": "test_user_123",
            "card_id": "Katze",
            "decision": "EASY",
            "timezone_name": "Europe/Dublin",
            "reset_interval": False
        }

        assert result == [
            {
                "status": "updated",
                "card_id": "Hund"
            },
            {
                "status": "updated",
                "card_id": "Katze"
            }
        ]


def test_process_review_session_processes_all_reviews(monkeypatch):
    calls = []

    def fake_review_flashcard(
        user_id,
        card_id,
        decision,
        timezone_name,
        reset_interval=False
    ):
        calls.append({
            "user_id": user_id,
            "card_id": card_id,
            "decision": decision,
            "timezone_name": timezone_name,
            "reset_interval": reset_interval
        })

        return {
            "status": "updated",
            "card_id": card_id
        }

    monkeypatch.setattr(
        "app.services.review_service.review_flashcard",
        fake_review_flashcard
    )

    reviews = [
        {
            "card_id": "Hund",
            "decision": "OK",
            "again_count": 0
        },
        {
            "card_id": "Katze",
            "decision": "EASY",
            "again_count": 0
        }
    ]

    result = process_review_session(
        "test_user_123",
        reviews,
        "Europe/Dublin"
    )

    assert len(calls) == 2

    assert calls[0] == {
        "user_id": "test_user_123",
        "card_id": "Hund",
        "decision": "OK",
        "timezone_name": "Europe/Dublin",
        "reset_interval": False
    }

    assert calls[1] == {
        "user_id": "test_user_123",
        "card_id": "Katze",
        "decision": "EASY",
        "timezone_name": "Europe/Dublin",
        "reset_interval": False
    }

    assert result == [
        {
            "status": "updated",
            "card_id": "Hund"
        },
        {
            "status": "updated",
            "card_id": "Katze"
        }
    ]


def test_process_review_session_does_not_reset_without_again(monkeypatch):
    received = {}

    def fake_review_flashcard(
        user_id,
        card_id,
        decision,
        timezone_name,
        reset_interval=False
    ):
        received["reset_interval"] = reset_interval

        return {
            "status": "updated"
        }

    monkeypatch.setattr(
        "app.services.review_service.review_flashcard",
        fake_review_flashcard
    )

    reviews = [
        {
            "card_id": "Hund",
            "decision": "OK",
            "again_count": 0
        }
    ]

    process_review_session(
        "test_user_123",
        reviews,
        "Europe/Dublin"
    )

    assert received["reset_interval"] is False

def test_process_review_session_defaults_again_count_to_zero(monkeypatch):
    received = {}

    def fake_review_flashcard(
        user_id,
        card_id,
        decision,
        timezone_name,
        reset_interval=False
    ):
        received["reset_interval"] = reset_interval

        return {
            "status": "updated"
        }

    monkeypatch.setattr(
        "app.services.review_service.review_flashcard",
        fake_review_flashcard
    )

    reviews = [
        {
            "card_id": "Hund",
            "decision": "OK"
        }
    ]

    process_review_session(
        "test_user_123",
        reviews,
        "Europe/Dublin"
    )

    assert received["reset_interval"] is False


def test_process_review_session_empty_list(monkeypatch):
    def fake_review_flashcard(*args, **kwargs):
        raise AssertionError(
            "review_flashcard should not be called"
        )

    monkeypatch.setattr(
        "app.services.review_service.review_flashcard",
        fake_review_flashcard
    )

    result = process_review_session(
        "test_user_123",
        [],
        "Europe/Dublin"
    )

    assert result == []



def test_review_flashcard_allows_due_card(monkeypatch):
    past_time = datetime(
        2020, 1, 1,
        0, 0,
        tzinfo=timezone.utc
    )

    monkeypatch.setattr(
        "app.services.review_service.get_flashcard",
        lambda user_id, card_id: {
            "interval_days": 3,
            "next_review_at": past_time
        }
    )

    monkeypatch.setattr(
        "app.services.review_service.process_review",
        lambda current_interval, decision, now, timezone_name: {
            "interval_days": 7,
            "next_review_at": datetime(
                2099, 1, 1,
                tzinfo=timezone.utc
            )
        }
    )

    monkeypatch.setattr(
        "app.services.review_service.update_flashcard_review",
        lambda user_id, card_id, interval_days, next_review_at: {
            "status": "updated",
            "card_id": card_id
        }
    )

    result = review_flashcard(
        "test_user_123",
        "Hund",
        "OK",
        "Europe/Dublin"
    )

    assert result == {
        "status": "updated",
        "card_id": "Hund"
    }

    def test_get_due_cards_for_user(monkeypatch):
        expected_cards = [
            {
                "card_id": "hund",
                "word": "Hund",
                "gender": "m"
            }
        ]

        def fake_get_due_flashcards(user_id, now):
            return expected_cards

        monkeypatch.setattr(
            "app.services.review_service.get_due_flashcards",
            fake_get_due_flashcards
        )

        result = get_due_cards_for_user(
            "test_user_123",
            "fake_now"
        )

        assert result == expected_cards

