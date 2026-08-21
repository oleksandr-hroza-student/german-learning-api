from app import create_app


#Here we are using a fixture (client from conftest.py)
#We do not need from tests.conftest import client
def test_health_flask(client):
    response = client.get("/api/health_flask")

    #Did the request succeed?
    assert response.status_code == 200
    #Did the request return corrects data?
    assert response.get_json() == {"status": "ok"}

