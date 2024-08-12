from typing import Protocol, List, Optional
from sensor_app.core.domain.entities import Sensor
from sensor_app.core.domain.results import AsyncResult


class BackgroundJobsRepository(Protocol):
    def send_task(self, task_name: str, *args, **kwargs) -> AsyncResult:
        pass

    def retry_task(self, task_id: str) -> AsyncResult:
        pass

    def get_task_results(self, task_id: str) -> AsyncResult:
        pass


class SensorRepository(Protocol):
    async def count_sensors(self) -> int:
        pass

    async def create_sensor(self, sensor: Sensor) -> Sensor:
        pass

    async def get_sensor(self, sensor_id: int) -> Optional[Sensor]:
        pass

    async def update_sensor(self, sensor: Sensor) -> Sensor:
        pass

    async def delete_sensor(self, sensor_id: int) -> None:
        pass

    async def list_sensors(self) -> List[Sensor]:
        pass

class SeedRepository(Protocol):
    async def initalize_database(self, seed_filepath: str) -> None:
        pass
