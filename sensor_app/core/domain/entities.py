from pydantic import BaseModel
from typing import Optional, Union


class Sensor(BaseModel):
    id: Optional[Union[int, str]] = None
    name: str
    value: float
