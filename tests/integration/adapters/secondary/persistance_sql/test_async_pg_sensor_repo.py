import pytest
from sensor_app.core.domain.entities import Sensor


@pytest.mark.asyncio
async def test_create_sensor(sensor_repo, test_logger):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_repo.create_sensor(sensor)
    assert created_sensor.id is not None
    assert created_sensor.name == "Test Sensor"
    assert created_sensor.value == 123.45


@pytest.mark.asyncio
async def test_get_sensor(sensor_repo):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_repo.create_sensor(sensor)
    fetched_sensor = await sensor_repo.get_sensor(created_sensor.id)
    assert fetched_sensor == created_sensor


@pytest.mark.asyncio
async def test_update_sensor(sensor_repo):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_repo.create_sensor(sensor)
    created_sensor.value = 678.90
    updated_sensor = await sensor_repo.update_sensor(created_sensor)
    assert updated_sensor.value == 678.90


@pytest.mark.asyncio
async def test_delete_sensor(sensor_repo):
    sensor = Sensor(name="Test Sensor", value=123.45)
    created_sensor = await sensor_repo.create_sensor(sensor)
    await sensor_repo.delete_sensor(created_sensor.id)
    deleted_sensor = await sensor_repo.get_sensor(created_sensor.id)
    assert deleted_sensor is None


@pytest.mark.asyncio
async def test_list_sensors(sensor_repo):
    sensor1 = Sensor(name="Test Sensor 1", value=123.45)
    sensor2 = Sensor(name="Test Sensor 2", value=678.90)
    await sensor_repo.create_sensor(sensor1)
    await sensor_repo.create_sensor(sensor2)
    sensors = await sensor_repo.list_sensors()
    assert len(sensors) >= 2
