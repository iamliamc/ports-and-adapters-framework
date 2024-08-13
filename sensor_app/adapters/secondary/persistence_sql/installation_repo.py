from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from sensor_app.core.domain.entities import Sensor, InstallationTimeline, DeviceState, DeviceType
from sensor_app.core.ports.secondary import InstallationRepository
import json
from datetime import datetime, timezone
import asyncpg  # type: ignore

class PostgresInstallationRepository(InstallationRepository):
    def __init__(self, database_url: str):
        self.database_url = database_url

    async def _get_connection(self) -> asyncpg.Connection:
        return await asyncpg.connect(self.database_url)

    async def create_installation_with_device_states(self, installation: InstallationTimeline, device_states: List[DeviceState]) -> InstallationTimeline:
        conn = await self._get_connection()
        async with conn.transaction():
            # Insert installation
            installation_id = await conn.fetchval(
                "INSERT INTO installations (name, effective_date) VALUES ($1, $2) RETURNING id",
                installation.name, installation.effective_date
            )
            installation.id = installation_id

            # Insert device states
            for state in device_states:
                device_state_id = await conn.fetchval(
                    "INSERT INTO device_states (installation_id, device_id, status, device_type_id) VALUES ($1, $2, $3, $4) RETURNING id",
                    installation_id, state.device_id, state.status.value, state.device_type_id
                )
                
                # Insert components
                for component in state.components:
                    await conn.execute(
                        "INSERT INTO components (device_state_id, name, serial_number, component_type_id) VALUES ($1, $2, $3, $4)",
                        device_state_id, component.name, component.serial_number, component.component_type_id
                    )

            return installation