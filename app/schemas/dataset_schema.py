from typing import Any 
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.schemas.dataset_definition import DatasetDefinition

class DatasetSchemaCreate(BaseModel):
    name: str
    description: str | None = None 
    definition: DatasetDefinition

class DatasetSchemaVersionCreate(BaseModel):
    description: str | None = None 
    definition: DatasetDefinition

class DatasetSchemaUpdate(BaseModel):
    description: str | None = None 

class DatasetSchemaResponse(BaseModel):
    schema_id: int
    schema_code: str
    name: str
    description: str | None
    version: int
    definition: DatasetDefinition
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)