from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Literal


class IngestionJobResponse(BaseModel):
    job_id: int

    dataset_id: int | None
    source_id: int | None

    operation_type: Literal[
        "append",
        "upsert",
        "replace",
        "delete"
    ]

    status: str

    started_at: datetime
    finished_at: datetime | None

    records_detected: int
    records_inserted: int
    records_updated: int
    records_deleted: int
    records_rejected: int

    error_message: str | None

    model_config = ConfigDict(from_attributes=True)