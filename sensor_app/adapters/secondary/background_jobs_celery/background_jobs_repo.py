# adapters.py
from celery import Celery
from sensor_app.core.ports.secondary import BackgroundJobsRepository
from sensor_app.settings import BackgroundJobsSettings

# Create a global singleton so this can be referenced in the repo and in sensor_app.main
_celery_app = None

def create_celery_app(background_job_settings: BackgroundJobsSettings):
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
            result_backend=background_job_settings.result_backend
        )

    return _celery_app

class CeleryBackgroundJobRepo(BackgroundJobsRepository):
    def __init__(self, background_job_settings: BackgroundJobsSettings):
        self.celery_app = create_celery_app(background_job_settings=background_job_settings)

    def send_task(self, task_name: str, *args, **kwargs):
        self.celery_app.send_task(task_name, args=args, kwargs=kwargs)