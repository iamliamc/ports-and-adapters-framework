import pytest
from fastapi.testclient import TestClient
from sensor_app.main import app


@pytest.fixture
def test_client(test_app):
    return TestClient(test_app)

def test_get_users(test_client, test_users):
    response = test_client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == len(test_users)