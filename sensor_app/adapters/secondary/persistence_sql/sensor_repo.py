import asyncpg  # type: ignore
from typing import List, Optional
from sensor_app.core.domain.entities import Sensor
from sensor_app.core.ports.secondary import SensorRepository


class AsyncpgSensorRepository(SensorRepository):
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def _get_connection(self) -> asyncpg.Connection:
        return await asyncpg.connect(self.database_url)

    async def count_sensors(self) -> int:
        conn = await self._get_connection()
        async with conn.transaction():
            row = await conn.fetchrow(
                "SELECT COUNT(*) from sensors",
            )
        await conn.close()
        return row

    async def create_sensor(self, sensor: Sensor) -> Sensor:
        conn = await self._get_connection()
        async with conn.transaction():
            row = await conn.fetchrow(
                "INSERT INTO sensors (name, value) VALUES ($1, $2) RETURNING id, name, value",
                sensor.name,
                sensor.value,
            )
        await conn.close()
        return Sensor(**row)

    async def get_sensor(self, sensor_id: int) -> Optional[Sensor]:
        conn = await self._get_connection()
        row = await conn.fetchrow(
            "SELECT id, name, value FROM sensors WHERE id = $1", sensor_id
        )
        await conn.close()
        if row:
            return Sensor(**row)
        return None

    async def update_sensor(self, sensor: Sensor) -> Sensor:
        conn = await self._get_connection()
        async with conn.transaction():
            row = await conn.fetchrow(
                "UPDATE sensors SET name = $1, value = $2 WHERE id = $3 RETURNING id, name, value",
                sensor.name,
                sensor.value,
                sensor.id,
            )
        await conn.close()
        return Sensor(**row)

    async def delete_sensor(self, sensor_id: int) -> None:
        conn = await self._get_connection()
        async with conn.transaction():
            await conn.execute("DELETE FROM sensors WHERE id = $1", sensor_id)
        await conn.close()

    async def list_sensors(self) -> List[Sensor]:
        conn = await self._get_connection()
        rows = await conn.fetch("SELECT id, name, value FROM sensors")
        await conn.close()
        return [Sensor(**row) for row in rows]
