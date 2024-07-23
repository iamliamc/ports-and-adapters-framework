from pydantic import BaseModel
from typing import Optional

class Sensor(BaseModel):
    id: Optional[int] = None
    name: str
    value: float