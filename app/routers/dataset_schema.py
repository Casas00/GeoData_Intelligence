from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.dataset_schema import (
    DatasetSchemaResponse,
    DatasetSchemaVersionCreate
)
from app.services.dataset_schema_service import (
    get_schemas,
    get_schema_by_code,
    get_schema_versions,
    create_schema_version
)

router = APIRouter(
    prefix='/dataset-schema',
    tags=["Dataset Schemas"]
)

@router.get("/", response_model=list[DatasetSchemaResponse])
def read_schemas(db:Session = Depends(get_db)):
    return get_schemas(db)

@router.get("/name/{schema_name}",response_model=list[DatasetSchemaResponse])
def read_schema_versions(
    schema_name:str,
    db:Session = Depends(get_db)
):
    schemas = get_schema_versions(db, schema_name)

    if not schemas:
        raise HTTPException(
            status_code=404,
            detail=f'Schemas with name "{schema_name}" not found'
        )

    return schemas

@router.get("/{schema_code}",response_model=DatasetSchemaResponse)
def read_schema_by_code(
    schema_code: str,
    db:Session = Depends(get_db)
):
    schema = get_schema_by_code(db,schema_code)

    if schema is None:
        raise HTTPException(
            status_code=404,
            detail=f'Schema with code "{schema_code}" not found',
        )

    return schema

@router.post("/name/{schema_name}/versions",response_model=DatasetSchemaResponse,status_code=201)
def create_new_schema_version(
    schema_name:str,
    schema_data: DatasetSchemaVersionCreate,
    db:Session = Depends(get_db)
):
    schema = create_schema_version(
        db,
        schema_name,
        schema_data
    )

    if schema is None:
        raise HTTPException(
            status_code=404,
            detail=f"Schema with name '{schema_name}' not found"
        )

    return schema