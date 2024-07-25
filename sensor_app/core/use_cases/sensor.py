from typing import List
from sensor_app.core.ports.primary import UseCase
from sensor_app.core.ports.secondary import SensorRepository, BackgroundJobsRepository
from sensor_app.core.domain.entities import Sensor


class ListSensors(UseCase):
    def __init__(self, sensor_repo: SensorRepository):
        self.sensor_repo = sensor_repo

    async def __call__(self) -> List[Sensor]:
        return await self.sensor_repo.list_sensors()


class CreateSensor(UseCase):
    def __init__(self, sensor_repo: SensorRepository):
        self.sensor_repo = sensor_repo

    async def __call__(self, sensor: Sensor) -> Sensor:
        return await self.sensor_repo.create_sensor(sensor)

class BigBackgroundJob(UseCase):
    def __init__(self, background_job_repo: BackgroundJobsRepository):
        self.background_job_repo = background_job_repo

    async def __call__(self, count: int) -> None:
        return await self.background_job_repo.send_task