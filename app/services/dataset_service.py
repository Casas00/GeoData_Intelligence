from sqlalchemy.orm import Session

from app.models.dataset import Dataset
from app.models.dataset_schema import DatasetSchema

def get_datasets(db:Session) -> list[Dataset]:
    """Retrieve all thematic datasets with their logical shemas"""

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