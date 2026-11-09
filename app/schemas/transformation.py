from datetime import datetime
from typing import Any
from pydantic import BaseModel, ConfigDict


class TransformationHistoryResponse(BaseModel):
    transformation_id: int
    job_id: int

    transformation_type: str
    description: str | None

    parameters: dict[str, Any] | None

    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)