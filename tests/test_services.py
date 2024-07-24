import pytest
import asyncio
from sensor_app.core.models import Sensor
from sensor_app.core.services import SensorService
from sensor_app.adapters.db_adapter import AsyncpgSensorRepository

@pytest.fixture
def sensor_service(database_url):
    repository = AsyncpgSensorRepository(database_url)
    return SensorService(repository)

@pytest.mark.asyncio
async def test_create_sensor(sensor_service):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_service.create_sensor(sensor)
    assert created_sensor.id is not None
    assert created_sensor.name == "Test Sensor"
    assert created_sensor.value == 123.45

@pytest.mark.asyncio
async def test_get_sensor(sensor_service):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_service.create_sensor(sensor)
    fetched_sensor = await sensor_service.get_sensor(created_sensor.id)
    assert fetched_sensor == created_sensor

@pytest.mark.asyncio
async def test_update_sensor(sensor_service):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_service.create_sensor(sensor)
    created_sensor.value = 678.90
    updated_sensor = await sensor_service.update_sensor(created_sensor)
    assert updated_sensor.value == 678.90

@pytest.mark.asyncio
async def test_delete_sensor(sensor_service):
    sensor = Sensor(name="Test Sensor", value=123.45

)
    created_sensor = await sensor_service.create_sensor(sensor)
    await sensor_service.delete_sensor(created_sensor.id)
    deleted_sensor = await sensor_service.get_sensor(created_sensor.id)
    assert deleted_sensor is None

@pytest.mark.asyncio
async def test_list_sensors(sensor_service):
    sensor1 = Sensor(name="Test Sensor 1", value=123.45)
    sensor2 = Sensor(name="Test Sensor 2", value=678.90)
    await sensor_service.create_sensor(sensor1)
    await sensor_service.create_sensor(sensor2)
    sensors = await sensor_service.list_sensors()
    assert len(sensors) >= 2