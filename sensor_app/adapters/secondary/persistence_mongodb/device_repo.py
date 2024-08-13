from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from sensor_app.core.domain.entities import Sensor, InstallationTimeline, DeviceType, DeviceState
from sensor_app.core.ports.secondary import DeviceRepository
import json
from datetime import datetime, timezone

class MongoDBDeviceRepository(DeviceRepository):
    def __init__(self, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client.get_default_database()
        self.collection = self.db.devices
        self.device_types_collection = self.db.device_types


    async def create(self, device: DeviceState) -> DeviceState:
        if device.device_type_id is None:
            raise ValueError("Device type ID is required")
        
        device_type = await self.device_types_collection.find_one({"uuid": device.device_type_id})
        device_type  = DeviceType.model_validate(device_type)
        import pdb; pdb.set_trace()
        # Match components to their component types
        for component in device.components:
            component.device_id = device.uuid
            if component.component_type_id is None:
                component_type = next(
                    (ct for ct in device_type.component_types if ct.name.lower() == component.name.lower()),
                    None
                )
                if component_type is None:
                    raise ValueError(f"Component type not found for component {component.name}")
            component.component_type_id = component_type.uuid

        # Convert Pydantic model to dictionary
        device_dict = device.model_dump(by_alias=True)
        
        # Remove the id field if it's None (let MongoDB generate it)
        device_dict.pop("device_type", None)
        current_time = datetime.now(timezone.utc)
        device_dict["created_at"] = current_time
        device_dict["updated_at"] = current_time
        result = await self.collection.insert_one(
            device_dict
        )

        # Update the id of the DeviceType object with the generated ObjectId
        device.id = str(result.inserted_id)

        return device