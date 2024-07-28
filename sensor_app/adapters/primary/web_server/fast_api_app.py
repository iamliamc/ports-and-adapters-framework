from typing import List
from fastapi import FastAPI, HTTPException
from uuid import UUID
from sensor_app.settings import WebServerSettings
from sensor_app.core.domain.entities import Sensor
from sensor_app.core.domain.results import AsyncResult
from sensor_app.core.ports.secondary import SensorRepository
from sensor_app.core.ports.secondary import BackgroundJobsRepository
from sensor_app.core.use_cases.sensor import CountSensors, GetSensor, ListSensors, CreateSensor
from sensor_app.core.use_cases.background_jobs import (
    GetBackgroundTaskResultsById,
    RetryBackgroundTaskById,
    StartBackgroundTask,
)
from fastapi.middleware.cors import CORSMiddleware
from random import randint


def create_fastapi_app(
    web_server_settings: WebServerSettings,
    sensor_repo: SensorRepository,
    background_jobs_repo: BackgroundJobsRepository,
) -> FastAPI:
    return app_factory(
        web_server_settings,
        count_sensors=CountSensors(sensor_repo=sensor_repo),
        get_sensor=GetSensor(sensor_repo=sensor_repo),
        list_sensors=ListSensors(sensor_repo=sensor_repo),
        create_sensor=CreateSensor(sensor_repo=sensor_repo),
        get_background_task_result_by_id=GetBackgroundTaskResultsById(
            background_jobs_repo=background_jobs_repo
        ),
        retry_background_task_by_id=RetryBackgroundTaskById(
            background_jobs_repo=background_jobs_repo
        ),
        start_background_task=StartBackgroundTask(
            background_jobs_repo=background_jobs_repo
        ),
    )


def app_factory(
    web_server_settings: WebServerSettings,
    count_sensors: CountSensors,
    get_sensor: GetSensor,
    list_sensors: ListSensors,
    create_sensor: CreateSensor,
    get_background_task_result_by_id: GetBackgroundTaskResultsById,
    retry_background_task_by_id: RetryBackgroundTaskById,
    start_background_task: StartBackgroundTask,
) -> FastAPI:
    # TODO pass configuration from WebServerSettings to FastAPI app
    app = FastAPI()

    # Define the origins that should be allowed to make requests to this app
    origins = [
        "http://localhost:5173",  # This if flexible-frontend
        "http://localhost:8000",  # Add other origins as needed
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Allow specific origins
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

    @app.get("/")
    def root() -> str:
        try:
            raise ValueError("Disaster")
        except ValueError as e:
            # Raise an HTTPException with status code 500 and an error message
            number = randint(0, 100)
            if number >= 50:
                raise HTTPException(status_code=500, detail=f"{e} {number}")
        return "Sensor App"

    @app.post("/retry_background_task", response_model=AsyncResult)
    async def use_retry_background_task_by_id(retry_background_task: AsyncResult):
        results = await retry_background_task_by_id(
            task_id=retry_background_task.task_id
        )
        return results

    # Technically we could hit flower API if so desired
    # https://flower.readthedocs.io/en/latest/api.html#get--api-task-info-(.*)
    # http://localhost:5555/api/task/info/f2b8b54e-fde2-4b78-aa1a-b6076dd5e31a
    @app.get("/background_task_results/{task_id}", response_model=AsyncResult)
    async def use_get_background_task_results(task_id: UUID):
        return await get_background_task_result_by_id(str(task_id))

    @app.get("/sensor_count")
    async def use_count_sensors():
        return await count_sensors()

    @app.get("/sensors", response_model=List[Sensor])
    async def use_list_sensors():
        return await list_sensors()
    
    @app.get("/sensor/{id}", response_model=Sensor)
    async def use_get_sensor(id: int) -> Sensor:
        sensor = await get_sensor(id)
        if sensor is None:
            raise HTTPException(status_code=404, detail=f"Sensor with {id} not found")
        return sensor

    @app.post("/sensor", response_model=Sensor)
    async def use_create_sensor(sensor: Sensor):
        return await create_sensor(sensor)

    @app.post("/make_one_thousand_sensors", response_model=AsyncResult)
    async def use_background_make_one_thousand_sensors():
        return await start_background_task("make_one_thousand_sensors")

    return app
