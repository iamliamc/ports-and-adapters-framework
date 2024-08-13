import logging
from typing import List, Optional
from sensor_app.core.ports.primary import UseCase
from sensor_app.core.ports.secondary import SeedRepository, DeviceTypeRepository, DeviceRepository, InstallationRepository
from sensor_app.core.domain.entities import Sensor, InstallationTimeline, DeviceType, DeviceStatus
import json
from uuid import uuid4

logger = logging.getLogger()


class SeedDatabase(UseCase):
    def __init__(self, device_type_repo: DeviceTypeRepository, device_repo: DeviceRepository, installation_repo: InstallationRepository):
        self.device_type_repo = device_type_repo
        self.device_repo = device_repo
        self.installation_repo = installation_repo

    async def __call__(self, seed_filepath: str) -> int:
        with open(seed_filepath, "r") as seed_file:
            data = json.load(seed_file)
            installations = [InstallationTimeline.model_validate(installation) for installation in data["installation_timelines"]]
            device_types = []
            device_states = []
            for installation in installations:
                device_type = installation.device_states[0].device_type
                device_type = await self.device_type_repo.create(device_type)
                device_types.append(device_type)
                for device_state in installation.device_states:
                    device_uuid = str(uuid4())
                    device_state.device_id = device_uuid
                    device_state.status = DeviceStatus.installed
                    device_state.device_type = device_type
                    device_state.device_type_id = device_type.uuid
                    # device = await self.device_repo.create(device_state)
                    for component in device_state.components:
                        component.device_id = device_uuid
                        if component.component_type_id is None:
                            component_type = next(
                                (ct for ct in device_type.component_types if ct.name.lower() == component.name.lower()),
                                None
                            )
                            if component_type is None:
                                raise ValueError(f"Component type not found for component {component.name}")
                        component.component_type_id = component_type.uuid
                    device_states.append(device_state)

                installation.device_states = device_states

                installation = await self.installation_repo.create(installation)

            import pdb; pdb.set_trace()
