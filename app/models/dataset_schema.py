from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    UniqueConstraint
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func

from app.database.base import Base


class DatasetSchema(Base):
    __tablename__ = "dataset_schemas"

    __table_args__ = (
        UniqueConstraint(
            "schema_code",
            name="uq_dataset_schemas_schema_code"
        ),
        UniqueConstraint(
            "name",
            "version",
            name="uq_dataset_schemas_name_version"
        ),
        {"schema": "metadata"}
    )

    schema_id = Column(Integer, primary_key=True, index=True)

    schema_code = Column(String(30), nullable=False)

    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)

    version = Column(Integer, nullable=False)

    definition = Column(JSONB, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )