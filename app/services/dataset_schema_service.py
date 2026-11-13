from sqlalchemy.orm import Session
from app.models.dataset_schema import DatasetSchema
from app.utils.schema_code_generator import (
    generate_schema_prefix,
    generate_alternative_prefix,
    generate_numeric_prefix,
    generate_version_code
)
from app.schemas.dataset_schema import DatasetSchemaCreate, DatasetSchemaUpdate

def schema_code_exists(db: Session, candidate: str) -> bool:
    return db.query(DatasetSchema).filter(
        DatasetSchema.schema_code == candidate
    ).first() is not None

def get_available_schema_code(db:Session,name:str,version:int) -> str:
    """Fin an avaibale scheam code in the database."""

    version_code = generate_version_code(version)

    # Level 1: First five letters
    prefix = generate_schema_prefix(name)
    candidate = f"{prefix}{version_code}"

    if not schema_code_exists(db, candidate):
        return candidate

    # Level 2: Three initial and two final letters
    prefix = generate_alternative_prefix(name)
    candidate = f"{prefix}{version_code}"

    if not schema_code_exists(db, candidate):
        return candidate

    # Level 3: Numeric suffix
    for suffix in range(1, 100):
        prefix = generate_numeric_prefix(name, suffix)
        candidate = f"{prefix}{version_code}"

        if not schema_code_exists(db, candidate):
            return candidate

    raise ValueError(
        f"Unable to generate an available schema code for '{name}'"
    )

def get_schema_by_id(db:Session, schemma_id: int) -> DatasetSchema | None:
    """Retrieve a logical schema by its database ID."""

    return db.query(DatasetSchema).filter(
        DatasetSchema.schema_id == schemma_id
    ).first()

def get_schema_by_code(db:Session, schema_code: str) -> DatasetSchema | None:
    """Retrieves a logical shcema by its unique code."""

    return db.query(DatasetSchema).filter(
        DatasetSchema.schema_code == schema_code
    ).first()    

def get_schemas(db:Session) -> list[DatasetSchema]:
    """Retrieves all logical schemas."""
    
    return db.query(DatasetSchema).order_by(
        DatasetSchema.name,
        DatasetSchema.version
    ).all()

def create_schema(db:Session,schema_data:DatasetSchemaCreate) -> DatasetSchema:
    """Create a new logical dataset schema."""

    #1. Check whether a schema with the same name already exists.
    existing_schema = db.query(DatasetSchema).filter(
        DatasetSchema.name == schema_data.name
    ).first()

    if existing_schema is not None:
        raise ValueError(
            f'A scheam named "{schema_data.name}" already exists.'
        )

    #2. Determine the initial version
    version = 1 

    #3. Generate an available schema code 
    schema_code = get_available_schema_code(
        db,
        schema_data.name,
        version
    )

    #4. Converte the Pydantic definition into a dictionary 
    definition = schema_data.definition.model_dump(mode='json')

    #5. Build the SQLAlchemy object
    new_schema = DatasetSchema(
        schema_code = schema_code,
        name= schema_data.name,
        description = schema_data.description,
        version=version,
        definition=definition
    )

    try:
        db.add(new_schema)
        db.commit()

        db.refresh(new_schema)

        return new_schema

    except Exception:
        db.rollback()
        raise


def get_schema_for_update(db: Session,schema_id: int | None = None,schema_code: str | None = None) -> DatasetSchema | None:
    """Retrieve a schema using its ID, code, or both."""

    # 1. Check that at least one identifier was provided
    if schema_id is None and schema_code is None:
        raise ValueError(
            "At least one identifier (schema_id or schema_code) "
            "must be provided."
        )

    # 2. Build the query
    query = db.query(DatasetSchema)

    if schema_id is not None:
        query = query.filter(
            DatasetSchema.schema_id == schema_id
        )

    if schema_code is not None:
        query = query.filter(
            DatasetSchema.schema_code == schema_code
        )

    # 3. Retrieve the matching schema
    schema = query.first()

    if schema is not None:
        return schema

    # 4. Check whether both identifiers refer to different records
    if schema_id is not None and schema_code is not None:

        schema_by_id = get_schema_by_id(db, schema_id)
        schema_by_code = get_schema_by_code(db, schema_code)

        if (
            schema_by_id is not None
            and schema_by_code is not None
            and schema_by_id.schema_id != schema_by_code.schema_id
        ):
            raise ValueError(
                "The provided schema_id and schema_code "
                "refer to different schemas."
            )

    return None



def update_schema(db: Session,schema_data: DatasetSchemaUpdate,schema_id: int | None = None, schema_code: str | None = None) -> DatasetSchema | None:
    """Update the description of an existing logical schema."""

    # 1. Retrieve the schema
    schema = get_schema_for_update(
        db,
        schema_id,
        schema_code
    )

    if schema is None:
        return None

    # 2. Check whether the description was provided
    if "description" not in schema_data.model_fields_set:
        raise ValueError(
            "No fields were provided for updating the schema."
        )

    # 3. Update the description
    schema.description = schema_data.description

    try:
        db.commit()
        db.refresh(schema)

        return schema

    except Exception:
        db.rollback()
        raise
