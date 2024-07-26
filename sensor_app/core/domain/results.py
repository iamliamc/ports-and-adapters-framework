from pydantic import BaseModel
from typing import Optional, Any


class AsyncResult(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    status: str
    result: Any
    traceback: Optional[str] = None
    args: Optional[Any] = None
    kwargs: Optional[Any] = None
    date_done: Optional[str] = None
