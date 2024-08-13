from datetime import datetime, timezone
from enum import Enum
from pydantic import UUID4, BaseModel, HttpUrl, Json, Field, model_validator
from typing import Optional, Tuple, Union, List, Any
from uuid import uuid4, UUID

def generate_uuid_str():
    return str(uuid4())

def get_current_utc_time():
    return datetime.now(timezone.utc)


class BaseModel(BaseModel):
    id: Optional[Any] = Field(default=None, alias="_id")

    @model_validator(mode='before')
    @classmethod
    def set_id(cls, data: Any):
        if isinstance(data, dict):
            if "_id" in data:
                data["id"] = str(data["_id"])
                del data["_id"]
        return data

class Sensor(BaseModel):
    id: Optional[Union[int, str]] = None
    name: str
    value: float

# class Installation(BaseModel):
#     id: Optional[Union[int, str]] = None
#     uuid: Optional[uuid4] = Field(default_factory=generate_uuid_str)
#     name: str
#     installation_date: datetime
#     removal_date: Optional[datetime] = None
#     location: Location
#     group: Optional['Group']
#     device: Device
#     created_at: Optional[Union[datetime]] = None
#     updated_at: Optional[Union[datetime]] = None

# class Component(BaseModel):
#     id: Optional[Union[int, str]] = None
#     uuid: str = Field(default_factory=generate_uuid_str)
#     name: str
#     serial_number: str
#     device_id: Optional[Union[int, str, uuid4]] = None
#     calibration_date: Optional[datetime] = None
#     installation_date: Optional[datetime] = None
#     component_type_id: Optional[Union[int, str]] = None

# class Device(BaseModel):
#     id: Optional[Union[int, str]] = None
#     uuid: str = Field(default_factory=generate_uuid_str)
#     device_type_id: Optional[Union[int, str]] = None
#     calibration_file: str
#     filename_prefix: str
#     notes: Optional[str] = None
#     components: List[Component]
#     status: Optional['DeviceStatus'] = None
#     device_type: 'DeviceType'  # Forward reference
#     created_at: Optional[Union[datetime]] = None
#     updated_at: Optional[Union[datetime]] = None

class GlobalMetadata(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = None
    time_coverage_start: Optional[datetime] = None
    time_coverage_end: Optional[datetime] = None
    creator_name: Optional[str] = None
    creator_contact: Optional[str] = None
    institution: Optional[str] = None
    geospatial_lat_max: Optional[float] = None
    geospatial_lat_min: Optional[float] = None
    geospatial_lat_units: Optional[str] = "degrees_north"
    geospatial_long_max: Optional[float] = None
    geospatial_long_min: Optional[float] = None
    geospatial_vertical_max: Optional[float] = None
    geospatial_vertical_min: Optional[float] = None
    geospatial_vertical_resolution: Optional[float] = None
    license: Optional[str] = None
    project: Optional[str] = None
    platform: Optional[str] = None
    version: Optional[float] = None
    publisher_url: Optional[str] = None
    creator_url: Optional[str] = None


class Location(BaseModel):
    id: Optional[Union[int, str]] = None
    name: str
    abbreviation: str
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class DeviceStatus(str, Enum):
    onboard = "onboard"
    installed = "installed"
    backup_ctd = "backup_ctd"
    sent_for_calibration = "sent_for_calibration"
    defective = "defective"
    lost = "lost"
    no_calibration_docs = "no_calibration_docs"

class DeviceState(BaseModel):
    id: Optional[Union[int, str]] = None
    device_id: Optional[uuid4] = None
    device_type_id: Optional[Union[int, str, uuid4]] = None
    calibration_file: str
    filename_prefix: str
    notes: Optional[str] = None
    components: List['ComponentState']
    status: Optional['DeviceStatus'] = None
    device_type: Optional['DeviceType'] = None  
    effective_date: Optional[datetime] = Field(default_factory=get_current_utc_time)
    expiration_date: Optional[datetime] = None
    created_at: Optional[Union[datetime]] = None
    updated_at: Optional[Union[datetime]] = None

class ComponentStatus(str, Enum):
    onboard = "onboard"
    installed = "installed"
    backup_ctd = "backup_ctd"
    sent_for_calibration = "sent_for_calibration"
    defective = "defective"
    lost = "lost"
    no_calibration_docs = "no_calibration_docs"

class ComponentState(BaseModel):
    id: Optional[Union[int, str]] = None
    component_id: Optional[Union[int, str, uuid4]] = Field(default_factory=generate_uuid_str)
    name: str
    serial_number: str
    device_id: Optional[Union[int, str, uuid4]] = None
    calibration_date: Optional[datetime] = None
    installation_date: Optional[datetime] = None
    removal_date: Optional[datetime] = None
    status: ComponentStatus
    component_type_id: Optional[Union[int, str]] = None
    ship_to_calibration_by: Optional[datetime] = None
    effecitve_date: Optional[datetime] = None
    expiration_date: Optional[datetime] = None

class Group(BaseModel):
    id: Optional[Union[int, str]] = None
    uuid: uuid4 = Field(default_factory=generate_uuid_str)
    name: str
    abbreviation: Optional[str]
    created_at: Optional[datetime] = Field(default_factory=get_current_utc_time)
    updated_at: Optional[datetime] = Field(default_factory=get_current_utc_time)
    notes: Optional[str] = None

# class GroupInstallations(BaseModel):
#     id: Optional[Union[int, str]]
#     uuid: uuid4 = Field(default_factory=generate_uuid_str)
#     label: str
#     abbreviation: Optional[str]
#     installation_timelines: List['InstallationTimeline']
#     group: Group
#     notes: Optional[str]

class InstallationTimeline(BaseModel):
    id: Optional[Union[int, str]] = None
    installation_id: Optional[uuid4] = Field(default_factory=generate_uuid_str)
    name: str
    installation_date: datetime
    removal_date: Optional[datetime] = None
    location: Location
    group: Group
    device_states: List[DeviceState]
    created_at: Optional[Union[datetime]] = None
    updated_at: Optional[Union[datetime]] = None

class UserRole(str, Enum):
    admin = "admin"
    technician = "technician"

class User(BaseModel):
    id: Optional[Union[int, str]]
    uuid: str = Field(default_factory=generate_uuid_str)
    role: UserRole
    email: str
    created_at: datetime
    updated_at: datetime

# class DeviceInstallation(BaseModel):
#     id: Optional[Union[int, str]]
#     device_identifier: UUID4
#     installation_id: Optional[Union[int, str]]
#     filename_prefix: str
#     installed_date: datetime
#     removal_date: Optional[datetime] = None
#     created_at: datetime
#     updated_at: datetime

class MeasurementType(BaseModel):
    id: Optional[Union[int, str]] = None
    uuid: str = Field(default_factory=generate_uuid_str)
    accuracy: Optional[Union[str, float]] = None
    alternative_label: Optional[str] = None
    description: Optional[str] = None
    header_label: Optional[str] = None
    label: str
    instrument_range: Optional[List[float]] = None
    resolution: Optional[float] = None
    type: Optional[str] = None
    units: str
    units_long: Optional[str] = None
    uri: Optional[str] = None

class ComponentType(BaseModel):
    id: Optional[Union[int, str]] = None
    uuid: str = Field(default_factory=generate_uuid_str)
    name: str
    label: str
    device_type_id: Optional[Union[int, str]] = None

class DeviceType(BaseModel):
    id: Optional[Union[int, str]] = None
    uuid: str = Field(default_factory=generate_uuid_str)
    label: str
    alternative_label: Optional[str] = None
    abbreviation: Optional[str] = None
    custom_device_reference: Optional[str] = None
    definition: Optional[str] = None
    instrument_type: str
    example_output: Optional[str] = None
    filename: Optional[str] = None
    file_header: Optional[str] = None
    identifier: str
    manual_link: Optional[str] = None
    parser: Optional[str] = None
    permit_parameters: List[str]
    uri: Optional[str] = None
    component_types: List[ComponentType]
    measurement_types: List[MeasurementType]
    created_at: Optional[Union[datetime]] = None
    updated_at: Optional[Union[datetime]] = None


# Device.model_rebuild()
# Installation.model_rebuild()

DeviceState.model_rebuild()
# GroupInstallations.model_rebuild()
InstallationTimeline.model_rebuild()