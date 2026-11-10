
from logging.config import fileConfig

from alembic import context

from app.database.base import Base
from app.database.connection import engine
import app.models

from sqlalchemy import text

# Configuración de Alembic
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Metadata de los modelos SQLAlchemy
target_metadata = Base.metadata


# Limitar la inspección al esquema metadata.
# Evita que Alembic interprete tablas ajenas al proyecto
# como elementos que deba eliminar.
def include_name(name, type_, parent_names):
    if type_ == "schema":
        return name == "metadata"

    return True


def run_migrations_offline() -> None:
    """Ejecuta las migraciones sin establecer una conexión directa."""

    context.configure(
        url=engine.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        include_schemas=True,
        compare_type=True,
        version_table_schema="metadata",
        include_name=include_name,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Ejecuta las migraciones utilizando una conexión activa."""

    with engine.connect() as connection:

        connection.execute(
            text("CREATE SCHEMA IF NOT EXISTS metadata")
        )
        connection.commit()

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            compare_type=True,
            version_table_schema="metadata",
            include_name=include_name,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
