#The intended behaviour for noun_service.py
#we imitate the response from the db, as it is a separate module's job
from app.services.noun_service import process_noun, process_multiple_nouns

def test_process_noun_found(monkeypatch):
    def fake_lookup_noun(noun):
        return [
            ("Hund", "m")
        ]

    monkeypatch.setattr(
        "app.services.noun_service.lookup_noun",
        fake_lookup_noun
    )

    result = process_noun("Hund")

    assert result == {
        "status": "found",
        "word": "Hund",
        "genders": ["m"]
    }

#We get 2 duplicates from the same route with the same gender
def test_process_noun_duplicate_same_gender(monkeypatch):
    def fake_lookup_noun(noun):
        return [
            ("Hund", "m"),
            ("Hund", "m")
        ]

    monkeypatch.setattr(
        "app.services.noun_service.lookup_noun",
        fake_lookup_noun
    )

    result = process_noun("Hund")

    assert result == {
        "status": "found",
        "word": "Hund",
        "genders": ["m"]
    }

#The word returns multiple genders
def test_process_noun_ambiguous(monkeypatch):
    def fake_lookup_noun(noun):
        return [
            ("Band", "m"),
            ("Band", "n")
        ]

    monkeypatch.setattr(
        "app.services.noun_service.lookup_noun",
        fake_lookup_noun
    )

    result = process_noun("Band")

    assert result == {
        "status": "ambiguous",
        "word": "Band",
        "genders": ["m", "n"]
    }


#process multiple nouns
def test_process_multiple_nouns(monkeypatch):
    def fake_process_noun(noun):
        fake_results = {
            "Hund": {
                "status": "found",
                "word": "Hund",
                "gender": "m"
            },
            "Katze": {
                "status": "found",
                "word": "Katze",
                "gender": "f"
            }
        }

        return fake_results[noun]

    monkeypatch.setattr(
        "app.services.noun_service.process_noun",
        fake_process_noun
    )

    result = process_multiple_nouns("Hund Katze")

    assert result == [
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

def test_process_noun_uses_ai_fallback_when_not_found(monkeypatch):
    received = {}

    def fake_lookup_noun(noun):
        return []

    def fake_resolve_noun_with_ai(noun):
        received["noun"] = noun

        return {
            "status": "found",
            "word": "Blorpo",
            "genders": ["n"]
        }

    monkeypatch.setattr(
        "app.services.noun_service.lookup_noun",
        fake_lookup_noun
    )

    monkeypatch.setattr(
        "app.services.noun_service.resolve_noun_with_ai",
        fake_resolve_noun_with_ai
    )

    result = process_noun("Blorpo")

    assert received["noun"] == "Blorpo"

    assert result == {
        "status": "found",
        "word": "Blorpo",
        "genders": ["n"]
    }

def test_process_noun_uses_ai_fallback_when_gender_missing(monkeypatch):
    def fake_lookup_noun(noun):
        return [
            ("Testwort", None)
        ]

    def fake_resolve_noun_with_ai(noun):
        return {
            "status": "found",
            "word": "Testwort",
            "genders": ["n"]
        }

    monkeypatch.setattr(
        "app.services.noun_service.lookup_noun",
        fake_lookup_noun
    )

    monkeypatch.setattr(
        "app.services.noun_service.resolve_noun_with_ai",
        fake_resolve_noun_with_ai
    )

    result = process_noun("Testwort")

    assert result == {
        "status": "found",
        "word": "Testwort",
        "genders": ["n"]
    }