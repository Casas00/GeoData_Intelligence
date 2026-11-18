from typing import Literal

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

    try:
        return type_mapping[field_type]
    except KeyError:
        raise ValueError(f'Unsupported field type: {field_type}')

def validate_common_definition(
    definition: DatasetDefinition
) -> None:
    """Validate rules shared by vector and tabular definitions."""

    reserved_fields = {'id','geom'}

    for field in definition.fields:
        if field.name.lower() in reserved_fields:
            raise ValueError(
                f'Field name "{field.name}" is reserved.'
            )


def validate_crs(
        db:Session,
        crs:str 
) -> None:
    """Validate that the CRS exists in PostGIS."""

    try:
        authority, code = crs.split(':',1)
        srid = int(code)
    except (ValueError, AttributeError):
        raise ValueError(
            f'Invalid CRS identifier: {crs}'
        )

    result = db.execute(
        text(""" 
            SELECT 1 
            FROM spatial_ref_sys
            WHERE auth_name = :authority
            AND auth_srid = :srid
        """),
        {
            'authority':authority.upper(),
            'srid':srid
        }
    ).first()

    if result is None:
        raise ValueError(
            f'CRS "{crs}" is not registered in PostGIS.'
        )

def validate_vector_definition(
    db:Session,
    definition: DatasetDefinition
) -> None:
    """Validate the spatial definition of a vector dataset."""

    if definition.geometry is None:
        raise ValueError(
            "A geometry definition is required for vector datasets."
        )

    if not definition.geometry.crs:
        raise ValueError(
            "A CRS must be defined for the geometry column."
        )

    validate_crs(db, definition.geometry.crs)

def validate_tabular_definition(
    definition: DatasetDefinition
) -> None:
    """Validate the definition of a non-spatial tabular dataset."""

    if definition.geometry is not None:
        raise ValueError(
            "Tabular datasets cannot contain a geometry definition."
        )

def validate_table_definition(
    db:Session,
    definition: DatasetDefinition,
    data_type: Literal['vector','tabular']
) -> None:
    """Validate a dataset definition according to its data type."""

    validate_common_definition(definition)

    if data_type == 'vector':
        validate_vector_definition(db,definition)

    elif data_type == 'tabular':
        validate_tabular_definition(definition)

    else:
        raise ValueError(
            f'Unsupported dataset type: {data_type}'
        )