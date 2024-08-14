from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from sensor_app.core.domain.entities import Sensor, InstallationTimeline, DeviceState, DeviceType
from sensor_app.core.ports.secondary import InstallationRepository
import json
from datetime import datetime, timezone

class MongoDBInstallationRepository(InstallationRepository):
    def __init__(self, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client.get_default_database()
        self.collection = self.db.installations


    async def create_installation_with_device_states(self, installation: InstallationTimeline) -> InstallationTimeline:

        # Convert Pydantic model to dictionary
        installation_dict = installation.model_dump(by_alias=True)

        # if installation.device.id is None:
        #     raise ValueError("Device ID is required")
        
        # if installation.device.device_type_id is None:
        #     raise ValueError("Device type ID is required")

        # Convert the Device object to a dictionary             
        import pdb; pdb.set_trace()

        current_time = datetime.now(timezone.utc)
        installation_dict["created_at"] = current_time
        installation_dict["updated_at"] = current_time

        result = await self.collection.insert_one(
            installation_dict
        )

        installation.id = str(result.inserted_id)

        return installation