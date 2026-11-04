from datetime import datetime, timezone

from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    UniqueConstraint
)

from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class DatasetSchema(Base):

    __tablename__ = "dataset_schemas"

    __table_args__ = (
        UniqueConstraint(
            "name",
            "version",
            name="uq_dataset_schema_name_version"
        ),
        {"schema": "metadata"}
    )

    # Primary Key
    schema_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # General Information
    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    version: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Logical Schema Definition
    definition: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )