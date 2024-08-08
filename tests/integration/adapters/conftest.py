import pytest
from fastapi.testclient import TestClient
from sensor_app.adapters.primary.web_server.fast_api_app import create_fastapi_app
from sensor_app.adapters.primary.background_job_server.celery_app import (
    create_celery_app,
)
from sensor_app.adapters.secondary.persistence_sql.sensor_repo import (
    AsyncpgSensorRepository,
)
from sensor_app.adapters.secondary.persistence_mongodb.sensor_repo import (
    MongoDBSensorRepository,
)
from sensor_app.adapters.secondary.background_jobs_celery.background_jobs_repo import (
    CeleryBackgroundJobRepo,
)


@pytest.fixture
def sensor_repo(conftest_settings):
    return AsyncpgSensorRepository(conftest_settings.database.connection)


@pytest.fixture
def no_sql_sensor_repo(conftest_settings):
    return MongoDBSensorRepository(conftest_settings.no_sql_database.connection)


@pytest.fixture
def background_jobs_repo(conftest_settings, test_background_jobs_worker):
    return CeleryBackgroundJobRepo(
        conftest_settings.background_jobs, test_background_jobs_worker
    )


@pytest.fixture
def test_app(conftest_settings, sensor_repo, background_jobs_repo):
    return create_fastapi_app(
        web_server_settings=conftest_settings.web_server_settings,
        sensor_repo=sensor_repo,
        background_jobs_repo=background_jobs_repo,
    )


@pytest.fixture
def test_background_jobs_worker(conftest_settings, sensor_repo):
    return create_celery_app(
        background_job_settings=conftest_settings.background_jobs,
        sensor_repo=sensor_repo,
    )


@pytest.fixture
def test_client(test_app):
    return TestClient(test_app)
