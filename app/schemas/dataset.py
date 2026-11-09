from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict


class DatasetCreate(BaseModel):
    name: str
    description: str | None = None

    schema_name: str
    table_name: str

    data_type: Literal["vector", "raster", "tabular"]

    geometry_type: str | None = None
    crs: str | None = None

    schema_id: int | None = None


class DatasetUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class DatasetResponse(BaseModel):
    dataset_id: int

    name: str
    description: str | None

    schema_name: str
    table_name: str

    data_type: Literal["vector", "raster", "tabular"]

    geometry_type: str | None
    crs: str | None

    schema_id: int | None

    status: str

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)