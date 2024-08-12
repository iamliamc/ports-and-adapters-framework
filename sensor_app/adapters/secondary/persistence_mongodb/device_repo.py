from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from sensor_app.core.domain.entities import Sensor, Installation, Device, DeviceType
from sensor_app.core.ports.secondary import DeviceRepository
import json

class MongoDBDeviceRepository(DeviceRepository):
    def __init__(self, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client.get_default_database()
        self.collection = self.db.devices
        self.device_types_collection = self.db.device_types


    async def create(self, device: Device) -> Device:
        # Convert Pydantic model to dictionary
        device_dict = device.model_dump(by_alias=True)
        
        # Remove the id field if it's None (let MongoDB generate it)
        device_dict.pop("device_type", None)

        if device.device_type_id is None:
            raise ValueError("Device type ID is required")
        
        device_type = await self.device_types_collection.find_one({"uuid": device.device_type_id})
        device_type  = DeviceType.model_validate(device_type)

        # Match components to their component types
        import pdb; pdb.set_trace()
        for component in device_dict.get("components", []):
            component_type_id = component.get("component_type_id")
            component_type = next((ct for ct in device_type["component_types"] if ct["_id"] == ObjectId(component_type_id)), None)
            if not component_type:
                raise ValueError(f"Invalid component type ID: {component_type_id}")
            component["component_type"] = component_type

        import pdb; pdb.set_trace()
        # Insert the document
        result = await self.collection.insert_one({
            **device_dict,
            "created_at": {"$currentDate": {"$type": "date"}},
            "updated_at": {"$currentDate": {"$type": "date"}}
        })

        # Update the id of the DeviceType object with the generated ObjectId
        device.id = str(result.inserted_id)

        return device