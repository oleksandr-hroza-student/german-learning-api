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
        "gender": "m"
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
        "gender": "m"
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

#No gender is found in the db
def test_process_noun_gender_missing(monkeypatch):
    def fake_lookup_noun(noun):
        return [
            ("Testwort", None)
        ]

    monkeypatch.setattr(
        "app.services.noun_service.lookup_noun",
        fake_lookup_noun
    )

    result = process_noun("Testwort")

    assert result == {
        "status": "gender_missing",
        "word": "Testwort"
    }


#Noun not in db
def test_process_noun_not_found(monkeypatch):
    def fake_lookup_noun(noun):
        return []

    monkeypatch.setattr(
        "app.services.noun_service.lookup_noun",
        fake_lookup_noun
    )

    result = process_noun("Blorpo")

    assert result == {
        "status": "not_found",
        "word": "Blorpo"
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