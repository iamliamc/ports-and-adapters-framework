from sensor_app.core.ports.secondary import BackgroundJobsRepository
from sensor_app.settings import BackgroundJobsSettings
from sensor_app.core.domain.results import AsyncResult
import celery.result as cr
from celery import Celery
from sensor_app.adapters.primary.background_job_server.celery_app import _celery_app


class CeleryBackgroundJobRepo(BackgroundJobsRepository):
    def __init__(
        self, background_job_settings: BackgroundJobsSettings, background_worker: Celery
    ):
        if background_worker is None:
            raise ValueError(
                "You must initialize create_celery_app before creating this repo"
            )
        self.celery_app = background_worker

    def send_task(self, task_name: str, *args, **kwargs) -> AsyncResult:
        task = self.celery_app.tasks[task_name]

        results = task.apply_async(args=args, kwargs=kwargs)
        return AsyncResult(
            id=results.id,
            name=results.name,
            status=results.status,
            result=results.result,
            traceback=results.traceback,
            args=results.args,
            kwargs=results.kwargs,
            date_done=results.date_done,
        )

    def retry_task(self, task_id: str) -> AsyncResult:
        meta = self.celery_app.backend.get_task_meta(task_id)
        task = self.celery_app.tasks[meta["name"]]
        results = task.apply_async(args=meta["args"], kwargs=meta["kwargs"])
        return AsyncResult(
            id=results.id,
            name=results.name,
            status=results.status,
            result=results.result,
            traceback=results.traceback,
            args=results.args,
            kwargs=results.kwargs,
            date_done=results.date_done,
        )

    def get_task_results(self, task_id: str) -> AsyncResult:
        meta = self.celery_app.backend.get_task_meta(task_id)
        results = cr.AsyncResult(task_id, app=self.celery_app)
        return AsyncResult(
            id=results.id,
            name=results.name,
            status=results.status,
            result=results.result,
            traceback=results.traceback,
            args=results.args,
            kwargs=results.kwargs,
            date_done=results.date_done,
        )
