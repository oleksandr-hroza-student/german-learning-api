from unittest.mock import MagicMock

from app.repositories.flashcard_repository import create_flashcard



def test_create_flashcard_creates_new_card(monkeypatch):
    fake_db = MagicMock()

    fake_card_ref = (
        fake_db.collection.return_value
        .document.return_value
        .collection.return_value
        .document.return_value
    )

    fake_card_doc = MagicMock()
    fake_card_doc.exists = False

    fake_card_ref.get.return_value = fake_card_doc

    monkeypatch.setattr(
        "app.repositories.flashcard_repository.get_db",
        lambda: fake_db
    )

    result = create_flashcard(
        "test_user_123",
        "Hund",
        "m"
    )

    fake_card_ref.set.assert_called_once_with({
        "word": "Hund",
        "gender": "m"
    })

    assert result == {
        "status": "created",
        "word": "Hund",
        "gender": "m"
    }


def test_create_flashcard_existing_card_not_overwritten(monkeypatch):
    fake_db = MagicMock()

    fake_card_ref = (
        fake_db.collection.return_value
        .document.return_value
        .collection.return_value
        .document.return_value
    )

    fake_card_doc = MagicMock()
    fake_card_doc.exists = True

    fake_card_ref.get.return_value = fake_card_doc

    monkeypatch.setattr(
        "app.repositories.flashcard_repository.get_db",
        lambda: fake_db
    )

    result = create_flashcard(
        "test_user_123",
        "Hund",
        "m"
    )

    fake_card_ref.set.assert_not_called()

    assert result == {
        "status": "already_exists",
        "word": "Hund"
    }

def test_create_flashcard_uses_correct_firestore_path(monkeypatch):
    fake_db = MagicMock()

    fake_card_ref = (
        fake_db.collection.return_value
        .document.return_value
        .collection.return_value
        .document.return_value
    )

    fake_card_doc = MagicMock()
    fake_card_doc.exists = False

    fake_card_ref.get.return_value = fake_card_doc

    monkeypatch.setattr(
        "app.repositories.flashcard_repository.get_db",
        lambda: fake_db
    )

    create_flashcard(
        "test_user_123",
        "HUND",
        "m"
    )

    fake_db.collection.assert_called_once_with("users")

    fake_db.collection.return_value.document.assert_called_once_with(
        "test_user_123"
    )

    fake_db.collection.return_value.document.return_value \
        .collection.assert_called_once_with("flashcards")

    fake_db.collection.return_value.document.return_value \
        .collection.return_value.document.assert_called_once_with(
            "hund"
        )