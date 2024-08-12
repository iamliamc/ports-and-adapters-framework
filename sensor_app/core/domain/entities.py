from datetime import date
from enum import Enum
from pydantic import UUID4, BaseModel, HttpUrl, Json
from typing import Optional, Tuple, Union, List


class Sensor(BaseModel):
    id: Optional[Union[int, str]] = None
    name: str
    value: float

class Location(BaseModel):
    id: int
    name: str
    abbreviation: str

class Group(BaseModel):
    id: str
    name: str

class Component(BaseModel):
    id: str
    name: str
    serial_number: str
    calibration_date: date
    installation_date: date
    component_type_id: str

class Device(BaseModel):
    calibration_file: str
    filename_prefix: str
    installation_date: date
    removal_date: Optional[date] = None
    notes: Optional[str] = None
    components: List[Component]
    device_type: 'DeviceType'  # Forward reference

class Installation(BaseModel):
    id: str
    uuid: UUID4
    name: str
    installation_date: date
    removal_date: Optional[date] = None
    effective_date: date
    end_date: Optional[date] = None
    location: Location
    group: Group
    device: Device

class UserRole(str, Enum):
    admin = "admin"
    technician = "technician"

class User(BaseModel):
    id: int
    role: UserRole
    email: str
    created_at: date
    updated_at: date

class GlobalMetadata(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    abstract: Optional[str] = None
    keywords: Optional[List[str]] = None
    time_coverage_start: Optional[date] = None
    time_coverage_end: Optional[date] = None
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
    id: int
    description: str
    abbreviated_description: str
    notes: Optional[str]
    created_at: date
    updated_at: date

class DeviceStatus(str, Enum):
    onboard = "onboard"
    installed = "installed"
    backup_ctd = "backup_ctd"
    sent_for_calibration = "sent_for_calibration"
    defective = "defective"
    lost = "lost"
    no_calibration_docs = "no_calibration_docs"

class DeviceState(BaseModel):
    id: int
    identifier: UUID4
    serial_number: UUID4
    device_type_id: int
    status: DeviceStatus
    start_date: date
    end_date: Optional[date]
    notes: Optional[str]

class DeviceInstallation(BaseModel):
    id: int
    device_identifier: UUID4
    installation_id: int
    filename_prefix: str
    installed_date: date
    removal_date: Optional[date] = None
    created_at: date
    updated_at: date

class DeviceTypeMeasurement(BaseModel):
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

class DeviceType(BaseModel):
    id: str
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
    device_type_measurements: List[DeviceTypeMeasurement]

class ComponentState(BaseModel):
    id: int
    identifier: UUID4
    serial_number: UUID4
    device_identifier: UUID4
    calibration_date: Optional[date]
    calibration_due: Optional[date]
    ship_to_calibration_by: Optional[date]
    installation_date: Optional[date]
    removal_date: Optional[date] = None
    start_date: date
    end_date: Optional[date]
    status: str
    component_type_id: int

class InstallationGroup(BaseModel):
    id: int
    label: str
    created_at: date
    updated_at: date
    notes: Optional[str]

class ComponentType(BaseModel):
    id: int
    device_type_id: int
    name: str