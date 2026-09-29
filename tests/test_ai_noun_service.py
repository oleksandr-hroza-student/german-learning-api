from app.services.ai_noun_service import parse_ai_noun_response, resolve_noun_with_ai
from app.services.flashcard_service import create_flashcards_from_text
import pytest

def test_parse_ai_noun_response_found():
    output_text = """
    {
        "status": "found",
        "word": "Hund",
        "genders": ["m"]
    }
    """

    result = parse_ai_noun_response(output_text)

    assert result == {
        "status": "found",
        "word": "Hund",
        "genders": ["m"]
    }

def test_parse_ai_noun_response_multiple_genders():
    output_text = """
    {
        "status": "found",
        "word": "Band",
        "genders": ["m", "n", "f"]
    }
    """

    result = parse_ai_noun_response(output_text)

    assert result == {
        "status": "found",
        "word": "Band",
        "genders": ["m", "n", "f"]
    }


def test_parse_ai_noun_response_not_a_noun():
    output_text = """
    {
        "status": "not_a_noun",
        "word": "Blorpo"
    }
    """

    result = parse_ai_noun_response(output_text)

    assert result == {
        "status": "not_a_noun",
        "word": "Blorpo"
    }



def test_parse_ai_noun_response_rejects_invalid_gender():
    output_text = """
    {
        "status": "found",
        "word": "Hund",
        "genders": ["x"]
    }
    """

    with pytest.raises(ValueError):
        parse_ai_noun_response(output_text)


def test_parse_ai_noun_response_rejects_invalid_status():
    output_text = """
    {
        "status": "maybe",
        "word": "Hund",
        "genders": ["m"]
    }
    """

    with pytest.raises(ValueError):
        parse_ai_noun_response(output_text)


def test_parse_ai_noun_response_rejects_invalid_json():
    output_text = """
    {
        "status": "found",
        "word": "Hund",
    """

    with pytest.raises(Exception):
        parse_ai_noun_response(output_text)

#WHat if AI gives us an error

def test_resolve_noun_with_ai_handles_api_error(monkeypatch):
    class FakeResponses:
        def create(self, *args, **kwargs):
            raise Exception("API unavailable")

    class FakeClient:
        responses = FakeResponses()

    monkeypatch.setattr(
        "app.services.ai_noun_service.OpenAI",
        lambda: FakeClient()
    )

    result = resolve_noun_with_ai("Blorpo")

    assert result == {
        "status": "ai_error"
    }


def test_create_flashcards_from_text_creates_ai_resolved_card(monkeypatch):
    received = {}

    def fake_process_multiple_nouns(text):
        return [
            {
                "status": "found",
                "word": "Miete",
                "genders": ["f"]
            }
        ]

    def fake_create_flashcard(user_id, word, genders):
        received["user_id"] = user_id
        received["word"] = word
        received["genders"] = genders

        return {
            "status": "created",
            "word": word,
            "genders": genders
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
        "Miete"
    )

    assert created == [
        {
            "status": "created",
            "word": "Miete",
            "genders": ["f"]
        }
    ]

    assert skipped == []

    assert received == {
        "user_id": "test_user_123",
        "word": "Miete",
        "genders": ["f"]
    }