from app.services.flashcard_service import create_flashcards_from_text

#Succesfully create flash cards from valid noun results
def test_create_flashcards_from_text_creates_valid_cards(monkeypatch):
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

    def fake_create_flashcard(user_id, word, gender):
        return {
            "status": "created",
            "word": word,
            "gender": gender
        }

    monkeypatch.setattr(
        "app.services.flashcard_service.process_multiple_nouns",
        fake_process_multiple_nouns
    )

    monkeypatch.setattr(
        "app.services.flashcard_service.create_flashcard",
        fake_create_flashcard
    )

    created, skipped = create_flashcards_from_text(
        "test_user_123",
        "Hund Katze"
    )

    assert created == [
        {
            "status": "created",
            "word": "Hund",
            "gender": "m"
        },
        {
            "status": "created",
            "word": "Katze",
            "gender": "f"
        }
    ]

    assert skipped == []

#In case process_multiple_nouns returns not_found/ambiguous/gender missing
def test_create_flashcards_from_text_skips_invalid_nouns(monkeypatch):
    def fake_process_multiple_nouns(text):
        return [
            {
                "status": "not_found",
                "word": "Blorpo"
            },
            {
                "status": "ambiguous",
                "word": "Band",
                "genders": ["m", "n"]
            },
            {
                "status": "gender_missing",
                "word": "Testwort"
            }
        ]

    def fake_create_flashcard(user_id, word, gender):
        raise AssertionError(
            "create_flashcard should not be called for invalid nouns"
        )

    monkeypatch.setattr(
        "app.services.flashcard_service.process_multiple_nouns",
        fake_process_multiple_nouns
    )

    monkeypatch.setattr(
        "app.services.flashcard_service.create_flashcard",
        fake_create_flashcard
    )

    created, skipped = create_flashcards_from_text(
        "test_user_123",
        "Blorpo Band Testwort"
    )

    assert created == []

    assert skipped == [
        {
            "status": "not_found",
            "word": "Blorpo"
        },
        {
            "status": "ambiguous",
            "word": "Band",
            "genders": ["m", "n"]
        },
        {
            "status": "gender_missing",
            "word": "Testwort"
        }
    ]

#In case the flash cards already exists, create_flashcard returns "already_exists"
def test_create_flashcards_from_text_skips_existing_card(monkeypatch):
    def fake_process_multiple_nouns(text):
        return [
            {
                "status": "found",
                "word": "Hund",
                "gender": "m"
            }
        ]

    def fake_create_flashcard(user_id, word, gender):
        return {
            "status": "already_exists",
            "word": word
        }

    monkeypatch.setattr(
        "app.services.flashcard_service.process_multiple_nouns",
        fake_process_multiple_nouns
    )

    monkeypatch.setattr(
        "app.services.flashcard_service.create_flashcard",
        fake_create_flashcard
    )

    created, skipped = create_flashcards_from_text(
        "test_user_123",
        "Hund"
    )

    assert created == []

    assert skipped == [
        {
            "status": "already_exists",
            "word": "Hund"
        }
    ]

#Here we prove that the service has passed the correct information downstream
def test_create_flashcards_from_text_passes_correct_data_to_repository(
    monkeypatch
):
    received = {}

    def fake_process_multiple_nouns(text):
        return [
            {
                "status": "found",
                "word": "Hund",
                "gender": "m"
            }
        ]

    def fake_create_flashcard(user_id, word, gender):
        received["user_id"] = user_id
        received["word"] = word
        received["gender"] = gender

        return {
            "status": "created",
            "word": word,
            "gender": gender
        }

    monkeypatch.setattr(
        "app.services.flashcard_service.process_multiple_nouns",
        fake_process_multiple_nouns
    )

    monkeypatch.setattr(
        "app.services.flashcard_service.create_flashcard",
        fake_create_flashcard
    )

    create_flashcards_from_text(
        "test_user_123",
        "Hund"
    )

    assert received == {
        "user_id": "test_user_123",
        "word": "Hund",
        "gender": "m"
    }
