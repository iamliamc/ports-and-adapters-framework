# adapters.py
import asyncio
from typing import Callable, TypeVar, List
from celery import Celery
from sensor_app.core.ports.secondary import SensorRepository
from sensor_app.settings import BackgroundJobsSettings
from sensor_app.core.use_cases.sensor import MakeOneThousandSensors

# Create a global singleton so this can be referenced in the repo and in sensor_app.main
_celery_app = None


T = TypeVar("T")


def run_async_task(async_func: Callable[..., T], *args, **kwargs) -> T:
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(async_func(*args, **kwargs))
    return result


def create_celery_task(
    celery_app: Celery, task_name: str, async_func: Callable[..., List]
) -> None:
    @celery_app.task(name=task_name)
    def celery_task(*args, **kwargs) -> List:
        return run_async_task(async_func, *args, **kwargs)


def configure_usecases_as_tasks(
    celery_app: Celery, make_one_thousand_sensors: MakeOneThousandSensors
) -> None:
    create_celery_task(
        celery_app,
        task_name="make_one_thousand_sensors",
        async_func=make_one_thousand_sensors,
    )
    return None


def create_celery_app(
    background_job_settings: BackgroundJobsSettings, sensor_repo: SensorRepository
) -> Celery:
    # TODO this poses an issue with tests...
    global _celery_app

    if _celery_app is None:
        _celery_app = Celery(
            background_job_settings.name,
            broker=background_job_settings.broker,
            backend=background_job_settings.backend,
        )

        # TODO do we only do this when not in production?
        _celery_app.conf.update(
            task_always_eager=background_job_settings.task_always_eager,
            task_eager_propagates=background_job_settings.task_eager_propagates,
            task_store_errors_even_if_ignored=True,
            broker_connection_retry_on_startup=background_job_settings.broker_connection_retry_on_startup,
            task_track_started=background_job_settings.task_track_started,
            task_send_sent_event=background_job_settings.task_send_sent_event,
            result_extended=True,
        )

        configure_usecases_as_tasks(
            celery_app=_celery_app,
            make_one_thousand_sensors=MakeOneThousandSensors(sensor_repo=sensor_repo),
        )

    return _celery_app
