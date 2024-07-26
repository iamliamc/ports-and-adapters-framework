import pytest
import logging
from fastapi.testclient import TestClient
from sensor_app.adapters.primary.web_server.fast_api_app import create_fastapi_app
from sensor_app.adapters.primary.background_job_server.celery_app import (
    create_celery_app,
)
from sensor_app.adapters.secondary.persistence_sql.sensor_repo import (
    AsyncpgSensorRepository,
)
from sensor_app.adapters.secondary.background_jobs_celery.background_jobs_repo import (
    CeleryBackgroundJobRepo,
)


def pytest_configure(config):
    logging.getLogger('celery').setLevel(logging.INFO)
    logging.getLogger('kombu').setLevel(logging.INFO)
    logging.getLogger('celery.utils.functional').setLevel(logging.WARNING)

@pytest.fixture
def sensor_repo(conftest_settings):
    return AsyncpgSensorRepository(conftest_settings.database.connection)


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


@pytest.fixture(scope="session")
def test_celery_worker(test_background_jobs_worker):
    # Create a Celery worker instance
    with test_background_jobs_worker.pool.acquire(block=True) as pool:
        yield
        pool.release()
