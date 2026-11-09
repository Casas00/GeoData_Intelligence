from typing import Any 
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class DatasetSchemaCreate(BaseModel):
    name: str
    description: str | None = None 
    definition: dict[str, Any]

class DatasetSchemaVersionCreate(BaseModel):
    description: str | None = None 
    definition: dict[str, Any]

class DatasetSchemaUpdate(BaseModel):
    description: str | None = None 
    definition: dict[str, Any] | None = None 

class DatasetSchemaResponse(BaseModel):
    schema_id: int
    schema_code: str
    name: str
    description: str | None
    version: int
    definition: dict[str, Any]
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)