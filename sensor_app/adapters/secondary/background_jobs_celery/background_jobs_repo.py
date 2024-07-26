# adapters.py
import asyncio
from celery import Celery
from sensor_app.core.ports.secondary import BackgroundJobsRepository
from sensor_app.core.ports.secondary import SensorRepository
from sensor_app.settings import BackgroundJobsSettings
from sensor_app.core.use_cases.sensor import MakeOneThousandSensors

# Create a global singleton so this can be referenced in the repo and in sensor_app.main
_celery_app = None

def configure_usecases_as_tasks(celery_app, sensor_repo) -> None:
    @celery_app.task(name='make_one_thousand_sensors')
    def make_one_thousand_sensors():
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(MakeOneThousandSensors(sensor_repo=sensor_repo)())
        return result

def create_celery_app(background_job_settings: BackgroundJobsSettings, sensor_repo: SensorRepository) -> Celery:
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
            broker_connection_retry_on_startup=background_job_settings.broker_connection_retry_on_startup
        )

        # Add logging?
        configure_usecases_as_tasks(
            celery_app=_celery_app,
            sensor_repo=sensor_repo,
            )


    return _celery_app

class CeleryBackgroundJobRepo(BackgroundJobsRepository):
    def __init__(self, background_job_settings: BackgroundJobsSettings):
        if _celery_app is None:
            raise ValueError("You must initialize create_celery_app before creating this repo")
        self.celery_app = _celery_app

    def send_task(self, task_name: str, *args, **kwargs):
        results = self.celery_app.send_task(task_name, args=args, kwargs=kwargs)
        return None