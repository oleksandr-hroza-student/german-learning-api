import pytest

from app.repositories.noun_repository import lookup_noun


@pytest.mark.integration
def test_lookup_noun_real_database():
    result = lookup_noun("Hund")

    assert len(result) > 0
    assert result[0][0] == "Hund"
    assert result[0][1] == "m"