# adapters.py
import asyncio
from celery import Celery
from sensor_app.core.ports.secondary import BackgroundJobsRepository
from sensor_app.core.ports.secondary import SensorRepository
from sensor_app.settings import BackgroundJobsSettings
from sensor_app.core.use_cases.sensor import MakeOneThousandSensors
from sensor_app.core.domain.results import AsyncResult

# Create a global singleton so this can be referenced in the repo and in sensor_app.main
_celery_app = None

def configure_usecases_as_tasks(celery_app, sensor_repo) -> None:
    @celery_app.task(name='make_one_thousand_sensors')
    def make_one_thousand_sensors():
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(MakeOneThousandSensors(sensor_repo=sensor_repo)())
        return AsyncResult(
            id=results.id,
            status=results.status,
            result=str(results.result),
            traceback=results.traceback,
            date_done=str(results.date_done)
        )

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
            task_store_errors_even_if_ignored=True,
            broker_connection_retry_on_startup=background_job_settings.broker_connection_retry_on_startup,
            task_track_started=background_job_settings.task_track_started,
            task_send_sent_event=background_job_settings.task_send_sent_event,
            result_extended=True,
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

    def send_task(self, task_name: str, *args, **kwargs) -> AsyncResult:
        results = self.celery_app.send_task(task_name, args=args, kwargs=kwargs)
        return results
    
    def retry_task(self, task_id: str) -> AsyncResult:
        meta = self.celery_app.backend.get_task_meta(task_id)
        task = self.celery_app.tasks[meta['name']]
        results = task.apply_async(args=meta['args'], kwargs=meta['kwargs'])
        return AsyncResult(
            id=results.id,
            name=meta['name'],
            status=results.status,
            result=str(results.result),
            traceback=results.traceback,
            args=meta['args'],
            kwargs=meta['kwargs'],
            date_done=str(results.date_done)
        )
