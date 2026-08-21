#Tests connection with firestore, more of an integration test, rather than unit test
import pytest
from app import create_app

@pytest.mark.integration
def test_health_firestore(client):
    response = client.get("api/health_firestore")
    data = response.get_json()
    assert data.get("success") == True
    assert response.status_code == 200