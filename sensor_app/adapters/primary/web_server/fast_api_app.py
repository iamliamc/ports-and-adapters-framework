from typing import List
from fastapi import FastAPI, Depends
from sensor_app.settings import WebServerSettings
from sensor_app.core.domain.entities import Sensor
from sensor_app.core.ports.secondary import SensorRepository
from sensor_app.core.ports.secondary import BackgroundJobsRepository
from sensor_app.core.use_cases.sensor import ListSensors, CreateSensor



def create_fastapi_app(
    web_server_settings: WebServerSettings, 
    sensor_repo: SensorRepository,
    background_job_repo: BackgroundJobsRepository
) -> FastAPI:
    return app_factory(
        web_server_settings,
        list_sensors=ListSensors(sensor_repo=sensor_repo),
        create_sensor=CreateSensor(sensor_repo=sensor_repo),
        big_background_job=BigBackgroundJob(background_job_repo=background_job_repo)
    )


def app_factory(
    web_server_settings: WebServerSettings,
    list_sensors: ListSensors,
    create_sensor: CreateSensor,
) -> FastAPI:
    # TODO pass configuration from WebServerSettings to FastAPI app
    app = FastAPI()

    @app.get("/")
    def root() -> str:
        return "Hello Sensor App"

    @app.get("/sensors", response_model=List[Sensor])
    async def use_list_sensors():
        return await list_sensors()

    @app.post("/sensor", response_model=Sensor)
    async def use_create_sensor(sensor: Sensor):
        return await create_sensor(sensor)

    return app
