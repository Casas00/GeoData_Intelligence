from app.database.connection import SessionLocal

from app.schemas.dataset_schema import DatasetSchemaUpdate
from app.services.dataset_schema_service import (
    get_schema_by_code,
    update_schema,
)


# Código de un esquema que ya existe en la base de datos.
# Esta prueba NO crea ningún registro.
SCHEMA_CODE = "PRUEB001"
NEW_DESCRIPTION = "Descripción actualizada mediante DatasetSchemaService."


db = SessionLocal()

try:
    # 1. Comprobar que el registro existe antes de intentar actualizarlo.
    existing_schema = get_schema_by_code(db, SCHEMA_CODE)

    if existing_schema is None:
        raise LookupError(
            f"No existe ningún DatasetSchema con schema_code={SCHEMA_CODE!r}. "
            "No se ha realizado ninguna actualización."
        )

    print("--- REGISTRO ANTES DE LA ACTUALIZACIÓN ---")
    print("ID:", existing_schema.schema_id)
    print("Código:", existing_schema.schema_code)
    print("Nombre:", existing_schema.name)
    print("Versión:", existing_schema.version)
    print("Descripción:", existing_schema.description)

    original_id = existing_schema.schema_id
    original_code = existing_schema.schema_code
    original_name = existing_schema.name
    original_version = existing_schema.version

    # 2. Actualizar únicamente la descripción, buscando por schema_code.
    updated_schema = update_schema(
        db,
        DatasetSchemaUpdate(description=NEW_DESCRIPTION),
        schema_code=SCHEMA_CODE,
    )

    if updated_schema is None:
        raise LookupError(
            f"No se ha encontrado el esquema {SCHEMA_CODE!r} para actualizarlo."
        )

    print("\\n--- RESULTADO DE LA ACTUALIZACIÓN ---")
    print("ID:", updated_schema.schema_id)
    print("Código:", updated_schema.schema_code)
    print("Nombre:", updated_schema.name)
    print("Versión:", updated_schema.version)
    print("Descripción:", updated_schema.description)

    # 3. Volver a consultar el registro para comprobar que el cambio se guardó.
    db.expire_all()
    persisted_schema = get_schema_by_code(db, SCHEMA_CODE)

    assert persisted_schema is not None
    assert persisted_schema.description == NEW_DESCRIPTION
    assert persisted_schema.schema_id == original_id
    assert persisted_schema.schema_code == original_code
    assert persisted_schema.name == original_name
    assert persisted_schema.version == original_version

    print("\\nPRUEBA CORRECTA: la descripción se ha actualizado y "
          "los datos de identificación y versión permanecen intactos.")

except Exception:
    db.rollback()
    raise

finally:
    db.close()
