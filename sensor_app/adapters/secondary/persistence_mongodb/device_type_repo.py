from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from sensor_app.core.domain.entities import Sensor, DeviceType
from sensor_app.core.ports.secondary import DeviceTypeRepository
import json
from datetime import datetime, timezone

class MongoDBDeviceTypeRepository(DeviceTypeRepository):
    def __init__(self, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client.get_default_database()
        self.collection = self.db.device_types

    async def create(self, device_type: DeviceType) -> DeviceType:
        # Convert Pydantic model to dictionary
        device_type_dict = device_type.model_dump(by_alias=True)

        # Remove the id field if it's None (let MongoDB generate it)
        device_type_dict.pop('id', None)

        # Set created_at and updated_at fields
        current_time = datetime.now(timezone.utc)
        device_type_dict["created_at"] = current_time
        device_type_dict["updated_at"] = current_time

        # Insert the document
        result = await self.collection.insert_one(device_type_dict)

        # Update the id of the DeviceType object with the generated ObjectId
        device_type.id = str(result.inserted_id)

        return device_type