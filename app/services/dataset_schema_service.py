from sqlalchemy.orm import Session
from app.models.dataset_schema import DatasetSchema
from app.utils.schema_code_generator import (
    generate_schema_prefix,
    generate_alternative_prefix,
    generate_numeric_prefix,
    generate_version_code
)

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

def create_schema(db,schema_data):

    pass

    #1. Validación de los datos recibidos 

    #2. Determianr la versión inicial
    
    #3. Generar el schema_code
    
    #4. Construir el objeto DatasetSchema
    
    #5. Guardar el registro en PostgreSQL
    
    #6. Confirmar la transacción 
    
    #7. Devolver DatasetSchemaResponse