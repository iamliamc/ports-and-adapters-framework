from typing import List
from sensor_app.core.models import Sensor
from sensor_app.core.ports import SensorRepository

class SensorService:
    def __init__(self, repository: SensorRepository):
        self.repository = repository

    async def create_sensor(self, sensor: Sensor) -> Sensor:
        return await self.repository.create_sensor(sensor)

    async def get_sensor(self, sensor_id: int) -> Sensor:
        return await self.repository.get_sensor(sensor_id)

    async def update_sensor(self, sensor: Sensor) -> Sensor:
        return await self.repository.update_sensor(sensor)

    async def delete_sensor(self, sensor_id: int) -> None:
        await self.repository.delete_sensor(sensor_id)

    async def list_sensors(self) -> List[Sensor]:
        return await self.repository.list_sensors()