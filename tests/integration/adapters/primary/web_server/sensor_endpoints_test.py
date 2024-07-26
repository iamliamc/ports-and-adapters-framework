import pytest
from fastapi.testclient import TestClient
from sensor_app.core.domain.entities import Sensor


def test_get_sensors(test_client):
    response = test_client.get("/sensors")
    assert response.status_code == 200
    assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_get_sensors_with_data(test_client, sensor_repo):

    await sensor_repo.create_sensor(Sensor(name="Test 1", value=200))

    response = test_client.get("/sensors")
    assert response.status_code == 200
    assert len(response.json()) == 1
