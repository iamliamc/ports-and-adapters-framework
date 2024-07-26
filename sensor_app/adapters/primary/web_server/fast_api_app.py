from typing import List
from fastapi import FastAPI, Depends
from uuid import UUID
from sensor_app.settings import WebServerSettings
from sensor_app.core.domain.entities import Sensor
from sensor_app.core.domain.results import AsyncResult
from sensor_app.core.ports.secondary import SensorRepository
from sensor_app.core.ports.secondary import BackgroundJobsRepository
from sensor_app.core.use_cases.sensor import CountSensors, ListSensors, CreateSensor
from sensor_app.core.use_cases.background_jobs import GetBackgroundTaskResultsById, RetryBackgroundTaskById, BackgroundMakeOneThousandSensors

def create_fastapi_app(
    web_server_settings: WebServerSettings, 
    sensor_repo: SensorRepository,
    background_jobs_repo: BackgroundJobsRepository
) -> FastAPI:
    return app_factory(
        web_server_settings,
        count_sensors=CountSensors(sensor_repo=sensor_repo),
        list_sensors=ListSensors(sensor_repo=sensor_repo),
        create_sensor=CreateSensor(sensor_repo=sensor_repo),
        get_background_task_result_by_id=GetBackgroundTaskResultsById(background_jobs_repo=background_jobs_repo),
        retry_background_task_by_id=RetryBackgroundTaskById(background_jobs_repo=background_jobs_repo),
        background_make_one_thousand_sensors=BackgroundMakeOneThousandSensors(background_jobs_repo=background_jobs_repo)
    )


def app_factory(
    web_server_settings: WebServerSettings,
    count_sensors: CountSensors,
    list_sensors: ListSensors,
    create_sensor: CreateSensor,
    get_background_task_result_by_id: GetBackgroundTaskResultsById,
    retry_background_task_by_id: RetryBackgroundTaskById,
    background_make_one_thousand_sensors: BackgroundMakeOneThousandSensors,

) -> FastAPI:
    # TODO pass configuration from WebServerSettings to FastAPI app
    app = FastAPI()

    @app.get("/")
    def root() -> str:
        return "Hello Sensor App"
    
    @app.post("/retry_background_task", response_model=AsyncResult)
    async def use_retry_background_task_by_id(retry_background_task: AsyncResult):
        results = await retry_background_task_by_id(task_id=retry_background_task.task_id)
        return results
    
    @app.get('/background_task_results/{task_id}')
    async def use_get_background_task_results(task_id: UUID):
        return await get_background_task_result_by_id(str(task_id))
    
    @app.get("/sensor_count")
    async def use_count_sensors():
        return await count_sensors()

    @app.get("/sensors", response_model=List[Sensor])
    async def use_list_sensors():
        return await list_sensors()

    @app.post("/sensor", response_model=Sensor)
    async def use_create_sensor(sensor: Sensor):
        return await create_sensor(sensor)
    
    @app.post("/make_one_thousand_sensors", response_model=AsyncResult)
    async def use_background_make_one_thousand_sensors():
        return await background_make_one_thousand_sensors()
    
    return app
