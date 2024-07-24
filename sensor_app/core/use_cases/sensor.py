from typing import List
from sensor_app.core.ports.primary import UseCase
from sensor_app.core.ports.secondary import SensorRepository
from sensor_app.core.domain.entities import Sensor

class ListSensors(UseCase):
    def __init__(
            self, sensor_repo: SensorRepository
    ):
        self.repo = sensor_repo

    async def __call__(self) -> List[Sensor]:
        return await self.repo.list_sensors()
        

class CreateSensor(UseCase):
    def __init__(
            self, sensor_repo: SensorRepository
    ):
        self.repo = sensor_repo

    async def __call__(self, sensor: Sensor) -> Sensor:
        return await self.repo.create_sensor(sensor)
