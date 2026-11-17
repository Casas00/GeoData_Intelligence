from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.dataset_definition import DatasetDefinition

def get_postgresql_type(field_type: str) -> str:
    """Translate a logical field type into a PostgreSQL data type."""

    type_mapping = {
        "integer": "INTEGER",
        "float": "DOUBLE PRECISION",
        "string": "VARCHAR",
        "boolean": "BOOLEAN",
        "date": "DATE",
        "datetime": "TIMESTAMP WITH TIME ZONE"
    }

    return type_mapping[field_type]


def validate_table_definition(
        defintion: DatasetDefinition
) -> None:
    pass