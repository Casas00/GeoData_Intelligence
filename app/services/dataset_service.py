from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.models.dataset_schema import DatasetSchema
from app.schemas.dataset import DatasetCreate

def get_datasets(db:Session) -> list[Dataset]:
    """Retrieve all thematic datasets"""

    return (
        db.query(Dataset)
        .order_by(Dataset.name)
        .all()
    )

def get_dataset_by_id(
    db:Session,
    dataset_id:int
) -> Dataset | None:
    """Retrieves a thematic dataset by its ID."""

    return (
        db.query(Dataset)
        .filter(Dataset.dataset_id == dataset_id)
        .first()
    )

def get_dataset_by_name(
        db:Session,
        name:str
) -> list[Dataset]:
    """Retieves thematic datasets by name"""

    return (
        db.query(Dataset)
        .filter(Dataset.name == name)
        .order_by(Dataset.name)
        .all()
    )

def get_datasets_by_schema(
    db: Session,
    schema_code: str
) -> list[Dataset]:
    """Retrieve thematic datasets associated with a logical schema."""

    return (
        db.query(Dataset)
        .join(Dataset.dataset_schema)
        .filter(DatasetSchema.schema_code == schema_code)
        .all()
    )

def create_dataset(
    db: Session,
    dataset_data: DatasetCreate
) -> Dataset | None:
    """Create a new thematic dataset metadata record."""

    schema = (
        db.query(DatasetSchema)
        .filter(
            DatasetSchema.schema_id == dataset_data.schema_id
        )
        .first()
    )

    if schema is None:
        return None

    new_dataset = Dataset(
        name=dataset_data.name,
        description=dataset_data.description,
        schema_name=dataset_data.schema_name,
        table_name=dataset_data.table_name,
        data_type=dataset_data.data_type,
        geometry_type=dataset_data.geometry_type,
        crs=dataset_data.crs,
        schema_id=dataset_data.schema_id
    )

    try:
        db.add(new_dataset)
        db.commit()
        db.refresh(new_dataset)

        return new_dataset

    except Exception:
        db.rollback()
        raise