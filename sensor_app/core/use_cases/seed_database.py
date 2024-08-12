import logging
from typing import List, Optional
from sensor_app.core.ports.primary import UseCase
from sensor_app.core.ports.secondary import SeedRepository, DeviceTypeRepository, DeviceRepository
from sensor_app.core.domain.entities import Sensor, Installation, DeviceType, DeviceStatus
import json


logger = logging.getLogger()


class SeedDatabase(UseCase):
    def __init__(self, device_type_repo: DeviceTypeRepository, device_repo: DeviceRepository):
        self.device_type_repo = device_type_repo
        self.device_repo = device_repo

    async def __call__(self, seed_filepath: str) -> int:
        with open(seed_filepath, "r") as seed_file:
            data = json.load(seed_file)
            installations = [Installation.model_validate(installation) for installation in data["installations"]]
            device_types = []
            for installation in installations:
                device = installation.device
                device.status = DeviceStatus.installed
                device_type = await self.device_type_repo.create(device.device_type)
                import pdb; pdb.set_trace()
                device.device_type = device_type
                device.device_type_id = device_type.uuid
                device = await self.device_repo.create(device)
                device_types.append(device_type)

            import pdb; pdb.set_trace()
