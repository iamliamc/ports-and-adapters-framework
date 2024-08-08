from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from sensor_app.core.domain.entities import Sensor
from sensor_app.core.ports.secondary import SensorRepository


class MongoDBSensorRepository(SensorRepository):
    def __init__(self, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client.get_default_database()
        self.collection = self.db.sensors

    async def count_sensors(self) -> int:
        return await self.collection.count_documents({})

    async def create_sensor(self, sensor: Sensor) -> Sensor:
        result = await self.collection.insert_one(
            {"name": sensor.name, "value": sensor.value}
        )
        sensor.id = str(result.inserted_id)
        return sensor

    async def get_sensor(self, sensor_id: int) -> Optional[Sensor]:
        result = await self.collection.find_one({"_id": ObjectId(str(sensor_id))})
        if result:
            return Sensor(
                id=str(result["_id"]), name=result["name"], value=result["value"]
            )
        return None

    async def update_sensor(self, sensor: Sensor) -> Sensor:
        result = await self.collection.find_one_and_update(
            {"_id": ObjectId(str(sensor.id))},
            {"$set": {"name": sensor.name, "value": sensor.value}},
            return_document=True,
        )
        if result:
            return Sensor(
                id=str(result["_id"]), name=result["name"], value=result["value"]
            )
        raise ValueError(f"Sensor with id {sensor.id} not found")

    async def delete_sensor(self, sensor_id: int) -> None:
        await self.collection.delete_one({"_id": ObjectId(str(sensor_id))})

    async def list_sensors(self) -> List[Sensor]:
        cursor = self.collection.find({})
        sensors = []
        async for document in cursor:
            sensors.append(
                Sensor(
                    id=str(document["_id"]),
                    name=document["name"],
                    value=document["value"],
                )
            )
        return sensors
