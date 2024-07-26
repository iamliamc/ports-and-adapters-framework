import logging
from typing import List
from sensor_app.core.ports.primary import UseCase
from sensor_app.core.ports.secondary import BackgroundJobsRepository
from sensor_app.core.domain.entities import Sensor

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
    
class BackgroundMakeOneThousandSensors(UseCase):
    def __init__(self, background_jobs_repo: BackgroundJobsRepository):
        self.background_jobs_repo = background_jobs_repo

    async def __call__(self) -> List[Sensor]:
        logger.info("Starting the background task to make one thousand sensors.")
        try:
            results = self.background_jobs_repo.send_task('make_one_thousand_sensors')
            logger.info("Background task completed successfully.")
            return results
        except Exception as e:
            logger.error(f"An error occurred while running the background task: {e}")
            raise