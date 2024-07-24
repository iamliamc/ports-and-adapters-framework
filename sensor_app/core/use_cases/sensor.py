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
        await self.repo.list_sensors()
        
