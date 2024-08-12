from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from sensor_app.core.domain.entities import Sensor, Installation, ComponentType
from sensor_app.core.ports.secondary import DeviceTypeRepository
import json

class MongoDBComponentTypeRepository(DeviceTypeRepository):
    def __init__(self, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client.get_default_database()
        self.collection = self.db.component_type

    async def create(self, component_type: ComponentType) -> ComponentType:
        # Convert Pydantic model to dictionary
        component_type_dict = component_type.model_dump(by_alias=True)

        # Remove the id field if it's None (let MongoDB generate it)
        component_type_dict.pop('id', None)

        if component_type.device_type_id is None:
            raise ValueError("Device type ID is required")

        # Insert the document
        result = await self.collection.insert_one(component_type_dict)

        # Update the id of the DeviceType object with the generated ObjectId
        component_type_dict.id = str(result.inserted_id)

        return component_type_dict