from pydantic import BaseModel
from typing import Optional


class RetryBackgroundTask(BaseModel):
    task_id: str

class Sensor(BaseModel):
    id: Optional[int] = None
    name: str
    value: float
