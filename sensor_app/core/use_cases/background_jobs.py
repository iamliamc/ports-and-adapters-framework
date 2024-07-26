import logging
from typing import List
from sensor_app.core.ports.primary import UseCase
from sensor_app.core.ports.secondary import BackgroundJobsRepository
from sensor_app.core.domain.results import AsyncResult

logger = logging.getLogger()


class RetryBackgroundTaskById(UseCase):
    def __init__(self, background_jobs_repo: BackgroundJobsRepository):
        self.background_jobs_repo = background_jobs_repo

    async def __call__(self, task_id: str):
        results = self.background_jobs_repo.retry_task(task_id)
        return results


class GetBackgroundTaskResultsById(UseCase):
    def __init__(self, background_jobs_repo: BackgroundJobsRepository):
        self.background_jobs_repo = background_jobs_repo

    async def __call__(self, task_id: str):
        results = self.background_jobs_repo.get_task_results(task_id)
        return results


class StartBackgroundTask(UseCase):
    def __init__(self, background_jobs_repo: BackgroundJobsRepository):
        self.background_jobs_repo = background_jobs_repo

    async def __call__(self, task_name: str) -> AsyncResult:
        logger.info(f"Starting the background task {task_name}.")
        try:
            results = self.background_jobs_repo.send_task(task_name=task_name)
            logger.info(f"Background task {task_name} entered queue successfully.")
            return results
        except Exception as e:
            logger.error(f"An error occurred while running the background task: {e}")
            raise
