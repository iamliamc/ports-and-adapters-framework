import logging
from typing import List
from sensor_app.core.ports.primary import UseCase
from sensor_app.core.ports.secondary import SensorRepository, BackgroundJobsRepository
from sensor_app.core.domain.entities import Sensor

logger = logging.getLogger()


class CountSensors(UseCase):
    def __init__(self, sensor_repo: SensorRepository):
        self.sensor_repo = sensor_repo

    async def __call__(self) -> int:
        return await self.sensor_repo.count_sensors()


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


class MakeOneThousandSensors(UseCase):
    def __init__(self, sensor_repo: SensorRepository):
        self.sensor_repo = sensor_repo

    async def __call__(self, count: int = 10) -> List[Sensor]:
        sensors = []
        for i in range(0, count):
            sensors.append(
                await self.sensor_repo.create_sensor(
                    Sensor(name=f"Sensor {i}", value=i)
                )
            )

        return sensors
