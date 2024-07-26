import pytest
from sensor_app.core.domain.entities import Sensor
from sensor_app.core.domain.results import AsyncResult


def test_send_task(sensor_repo, background_jobs_repo, test_logger):
    results = background_jobs_repo.send_task("make_one_thousand_sensors", count=5)
    assert isinstance(results, AsyncResult)
    assert len(results.result) == 5
    assert results.status == "SUCCESS"
