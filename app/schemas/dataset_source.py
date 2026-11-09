from datetime import datetime
from pydantic import BaseModel, ConfigDict

class DatasetSourceCreate(BaseModel):
    source_name: str
    source_type: str

    source_format: str | None = None
    source_url: str | None = None 
    file_path: str | None = None 
    file_size: int | None = None 
    file_hash: str | None = None 

class DatasetSourceUpdate(BaseModel):
    source_name: str | None = None
    source_type: str | None = None
    source_format: str | None = None
    source_url: str | None = None 

class DatasetSourceResponse(BaseModel):
    source_id: int 
    dataset_id: int 

    source_name: str
    source_type: str

    source_format: str | None 
    source_url: str | None
    file_path: str | None 
    file_size: int | None 
    file_hash: str | None 

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)