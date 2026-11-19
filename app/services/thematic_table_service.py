import re
from typing import Literal

from sqlalchemy import text
from sqlalchemy.orm import Session

from app.schemas.dataset_definition import DatasetDefinition, FieldDefinition


DatasetType = Literal["vector", "tabular"]
_IDENTIFIER_PATTERN = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


class ThematicTableAlreadyExistsError(Exception):
    """Raised when a thematic table already exists."""


def validate_sql_identifier(identifier: str, label: str) -> None:
    """Validate a PostgreSQL identifier before interpolating it into SQL."""
    if not isinstance(identifier, str) or not _IDENTIFIER_PATTERN.fullmatch(identifier):
        raise ValueError(f"Invalid {label}: {identifier!r}")
    if len(identifier.encode("utf-8")) > 63:
        raise ValueError(f"{label.capitalize()} exceeds PostgreSQL's 63-byte identifier limit.")


def get_postgresql_type(field_type: str) -> str:
    """Translate a logical field type into a PostgreSQL data type."""
    type_mapping = {
        "integer": "INTEGER",
        "float": "DOUBLE PRECISION",
        "string": "VARCHAR",
        "boolean": "BOOLEAN",
        "date": "DATE",
        "datetime": "TIMESTAMP WITH TIME ZONE",
    }
    try:
        return type_mapping[field_type]
    except KeyError:
        raise ValueError(f"Unsupported field type: {field_type}") from None


def validate_common_definition(definition: DatasetDefinition) -> None:
    """Validate rules shared by vector and tabular definitions."""
    reserved_fields = {"id", "geom"}
    for field in definition.fields:
        if field.name.lower() in reserved_fields:
            raise ValueError(f'Field name "{field.name}" is reserved.')


def validate_crs(db: Session, crs: str) -> None:
    """Validate that an EPSG CRS exists in PostGIS."""
    try:
        authority, code = crs.strip().split(":", 1)
        srid = int(code)
    except (ValueError, AttributeError):
        raise ValueError(f"Invalid CRS identifier: {crs}") from None
    if authority.upper() != "EPSG" or srid <= 0:
        raise ValueError(f"Invalid EPSG CRS identifier: {crs}")

    result = db.execute(
        text(
            """
            SELECT 1
            FROM spatial_ref_sys
            WHERE UPPER(auth_name) = :authority
              AND auth_srid = :srid
            """
        ),
        {"authority": "EPSG", "srid": srid},
    ).first()
    if result is None:
        raise ValueError(f'CRS "{crs}" is not registered in PostGIS.')


def get_crs_srid(crs: str) -> int:
    """Extract the numeric SRID from an EPSG identifier."""
    try:
        authority, code = crs.strip().split(":", 1)
        srid = int(code)
    except (ValueError, AttributeError):
        raise ValueError(f"Invalid CRS identifier: {crs}") from None
    if authority.upper() != "EPSG" or srid <= 0:
        raise ValueError(f"Unsupported or invalid CRS identifier: {crs}")
    return srid


def validate_vector_definition(db: Session, definition: DatasetDefinition) -> None:
    """Validate the spatial definition of a vector dataset."""
    if definition.geometry is None:
        raise ValueError("A geometry definition is required for vector datasets.")
    if not definition.geometry.crs:
        raise ValueError("A CRS must be defined for the geometry column.")
    # GeometryDefinition's Pydantic Literal validates the allowed geometry types.
    validate_crs(db, definition.geometry.crs)


def validate_tabular_definition(definition: DatasetDefinition) -> None:
    """Validate the definition of a non-spatial tabular dataset."""
    if definition.geometry is not None:
        raise ValueError("Tabular datasets cannot contain a geometry definition.")


def validate_table_definition(
    db: Session,
    definition: DatasetDefinition,
    data_type: DatasetType,
) -> None:
    """Validate a dataset definition according to its data type."""
    validate_common_definition(definition)
    if data_type == "vector":
        validate_vector_definition(db, definition)
    elif data_type == "tabular":
        validate_tabular_definition(definition)
    else:
        raise ValueError(f"Unsupported dataset type: {data_type}")


def build_field_sql(field: FieldDefinition) -> str:
    """Build a SQL column definition from a field definition."""
    validate_sql_identifier(field.name, "field name")
    postgresql_type = get_postgresql_type(field.type)
    nullability = "NOT NULL" if field.required else "NULL"
    return f'"{field.name}" {postgresql_type} {nullability}'


def build_table_sql(
    definition: DatasetDefinition,
    schema_name: str,
    table_name: str,
    data_type: DatasetType,
) -> str:
    """Build the SQL statement for creating a thematic table."""
    validate_sql_identifier(schema_name, "schema name")
    validate_sql_identifier(table_name, "table name")
    if data_type not in ("vector", "tabular"):
        raise ValueError(f"Unsupported dataset type: {data_type}")
    if data_type == "vector" and definition.geometry is None:
        raise ValueError("A geometry definition is required for vector datasets.")
    if data_type == "tabular" and definition.geometry is not None:
        raise ValueError("Tabular datasets cannot contain a geometry definition.")

    columns = ['"id" BIGINT GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY']
    columns.extend(build_field_sql(field) for field in definition.fields)

    if data_type == "vector":
        geometry = definition.geometry
        srid = get_crs_srid(geometry.crs)
        geometry_nullability = "NULL" if geometry.nullable else "NOT NULL"
        columns.append(f'"geom" geometry({geometry.type}, {srid}) {geometry_nullability}')

    columns_sql = ",\n    ".join(columns)
    return (
        f'CREATE TABLE "{schema_name}"."{table_name}" (\n'
        f"    {columns_sql}\n"
        ");"
    )


def ensure_schema_exists(db: Session, schema_name: str) -> None:
    """Create the PostgreSQL schema if it does not exist."""
    validate_sql_identifier(schema_name, "schema name")
    db.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{schema_name}"'))


def create_thematic_table(
    db: Session,
    definition: DatasetDefinition,
    schema_name: str,
    table_name: str,
    data_type: Literal['vector','tabular']
) -> None:
    """Create a thematic table and its spatial index when applicable."""

    validate_sql_identifier(schema_name, "schema_name")
    validate_sql_identifier(table_name,'table_name')

    validate_table_definition(db, definition, data_type)

    ensure_schema_exists(db, schema_name)

    qualified_name = f'"{schema_name}"."{table_name}"'

    result = db.execute(
        text("SELECT to_regclass(:qualified_name)"),
        {"qualified_name":qualified_name}
    ).scalar_one()

    if result is not None:
        raise ThematicTableAlreadyExistsError(
            f'Table "{qualified_name}" alredy exists.'
        )

    sql = build_table_sql(
        definition,
        schema_name,
        table_name,
        data_type
    )

    db.execute(text(sql))

    if data_type == 'vector':
        db.execute(
            text(
                f'CREATE INDEX ON "{schema_name}"."{table_name}" '
                'USING GIST ("geom")' 
            )
        )