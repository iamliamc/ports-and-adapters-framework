from typing import Protocol, List
from sensor_app.core.domain.entities import Sensor


class SensorRepository(Protocol):
    async def create_sensor(self, sensor: Sensor) -> Sensor:
        pass

    async def get_sensor(self, sensor_id: int) -> Sensor:
        pass

    async def update_sensor(self, sensor: Sensor) -> Sensor:
        pass

    async def delete_sensor(self, sensor_id: int) -> None:
        pass

    async def list_sensors(self) -> List[Sensor]:
        pass
