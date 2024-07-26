from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime
import json
import logging

logger = logging.getLogger()


class AsyncResult(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    status: str
    result: Any
    traceback: Optional[str] = None
    args: Optional[Any] = None
    kwargs: Optional[Any] = None
    date_done: Optional[datetime] = None

    def __init__(self, **data):
        super().__init__(**data)
        # Attempt to serialize the `result` field
        self.result = self.serialize_result(self.result) or self.result

    def serialize_result(self, result: Any) -> str:
        if isinstance(result, BaseModel):
            # If the result is a BaseModel, skip serialization
            return result
        elif isinstance(result, list) and all(
            isinstance(item, BaseModel) for item in result
        ):
            # If the result is a list of BaseModels, skip serialization
            return result
        else:
            try:
                # Attempt to serialize `result` directly
                json.dumps(result)
            except Exception as e:
                logger.warning(f"Problem serializing AsyncResult {self.id} error: {e}")
                return str(result)
            return None
