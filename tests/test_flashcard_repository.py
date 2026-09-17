from unittest.mock import MagicMock
from firebase_admin import firestore
from app.repositories.flashcard_repository import create_flashcard, get_all_flashcards, delete_flashcard



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
        "gender": "m",
        "interval_days": 0,
        "next_review_at": firestore.SERVER_TIMESTAMP,
        "last_reviewed_at": None,
        "review_count": 0
    })
    """
    """

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
        .collection.return_value.document.assert_called_once_with("hund")



def test_get_all_flashcards_returns_cards(monkeypatch):
    fake_db = MagicMock()

    fake_cards_ref = (
        fake_db.collection.return_value
        .document.return_value
        .collection.return_value
    )

    doc1 = MagicMock()
    doc1.to_dict.return_value = {
        "word": "Hund",
        "gender": "m"
    }

    doc2 = MagicMock()
    doc2.to_dict.return_value = {
        "word": "Katze",
        "gender": "f"
    }

    fake_cards_ref.stream.return_value = [doc1, doc2]

    monkeypatch.setattr(
        "app.repositories.flashcard_repository.get_db",
        lambda: fake_db
    )

    result = get_all_flashcards("test_user_123")

    assert result == [
        {
            "word": "Hund",
            "gender": "m"
        },
        {
            "word": "Katze",
            "gender": "f"
        }
    ]



def test_delete_flashcard_deletes_existing_card(monkeypatch):
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

    result = delete_flashcard(
        "test_user_123",
        "Hund"
    )

    fake_card_ref.delete.assert_called_once()

    assert result == {
        "status": "deleted",
        "card_id": "Hund"
    }


def test_delete_flashcard_missing_card(monkeypatch):
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

    result = delete_flashcard(
        "test_user_123",
        "Hund"
    )

    fake_card_ref.delete.assert_not_called()

    assert result == {
        "status": "not_found",
        "card_id": "Hund"
    }


def test_delete_flashcard_uses_correct_path(monkeypatch):
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

    delete_flashcard(
        "test_user_123",
        "HUND"
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