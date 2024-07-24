import pytest
from fastapi.testclient import TestClient
from sensor_app.main import app
from sensor_app.adapters.primary.web_server.fast_api_app import create_fastapi_app
from sensor_app.adapters.secondary.persistence_sql.sensor_repo import (
    AsyncpgSensorRepository,
)


@pytest.fixture
def test_sensor_repo(conftest_settings):
    return AsyncpgSensorRepository(conftest_settings.database.connection)


@pytest.fixture
def test_app(conftest_settings, test_sensor_repo):
    return create_fastapi_app(
        web_server_settings=conftest_settings.web_server_settings,
        sensor_repo=test_sensor_repo,
    )
