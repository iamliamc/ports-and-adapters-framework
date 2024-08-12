import logging
from typing import List, Optional
from sensor_app.core.ports.primary import UseCase
from sensor_app.core.ports.secondary import SeedRepository, BackgroundJobsRepository
from sensor_app.core.domain.entities import Sensor

logger = logging.getLogger()


class SeedDatabase(UseCase):
    def __init__(self, seed_repo: SeedRepository):
        self.seed_repo = seed_repo

    async def __call__(self, seed_filepath: str) -> int:
        return await self.seed_repo.initalize_database(seed_filepath=seed_filepath)
