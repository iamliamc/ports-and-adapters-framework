from typing import List
from fastapi import FastAPI
from sensor_app.settings import WebServerSettings
from sensor_app.core.domain.entities import Sensor
from sensor_app.core.ports.secondary import SensorRepository
from sensor_app.core.use_cases.sensor import ListSensors

def create_fastapi_app(web_server_settings: WebServerSettings, sensor_repo: SensorRepository) -> FastAPI:
    # TODO pass configuration from WebServerSettings to FastAPI app
    app = FastAPI()

    @app.get("/")
    def read_root() -> str:
        return "Hello Sensor App"

    @app.get("/sensors") 
    async def list_sensors() -> List[Sensor]:
        return await ListSensors(sensor_repo)
    
    return app
    