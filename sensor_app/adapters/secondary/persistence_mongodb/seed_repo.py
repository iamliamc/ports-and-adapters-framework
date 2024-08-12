from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from sensor_app.core.domain.entities import Sensor, Installation
from sensor_app.core.ports.secondary import SeedRepository
import json

class MongoDBSeedRepository(SeedRepository):
    def __init__(self, connection_string: str):
        self.client = AsyncIOMotorClient(connection_string)
        self.db = self.client.get_default_database()


    async def initalize_database(self, seed_filepath: str) -> None:
        with open(seed_filepath, "r") as seed_file:
            data = json.load(seed_file)
            installations = [Installation.model_validate(installation) for installation in data["installations"]]
            import pdb; pdb.set_trace()
