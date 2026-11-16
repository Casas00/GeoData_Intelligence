from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.dataset import DatasetResponse

from app.services.dataset_service import (
    get_datasets,
    get_dataset_by_id,
    get_dataset_by_name,
    get_datasets_by_schema
)

router = APIRouter(
    prefix='/datasets',
    tags=['Datasets']
)

@router.get('/',response_model=list[DatasetResponse])
def read_datasets(db:Session = Depends(get_db)):
    return get_datasets(db)

@router.get("/name/{name}",response_model=list[DatasetResponse])
def read_datasets_by_name(
    name:str,
    db:Session = Depends(get_db)
):
    datasets =  get_dataset_by_name(db,name)

    if not datasets:
        raise HTTPException(
            status_code = 404,
            detail=f'No daatsets found with name "{name}"'
        )

    return datasets

@router.get("/schema/{schema_code}",response_model=list[DatasetResponse])
def read_datasets_by_schema(
    schema_code:str,
    db:Session = Depends(get_db)
):
    datasets = get_datasets_by_schema(db,schema_code)

    if not datasets:
        raise HTTPException(
            status_code = 404,
            detail=f'No daatsets found with schema code "{schema_code}"'
        )

    return datasets

@router.get("/{dataset_id}",response_model=DatasetResponse)
def read_datasets_by_id(
    dataset_id:int,
    db:Session = Depends(get_db)
):
    dataset = get_dataset_by_id(db,dataset_id)

    if dataset is None:
        raise HTTPException(
            status_code=404,
            detail=f'Dataset with ID "{dataset_id}" not found'
        )

    return dataset