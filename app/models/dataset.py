from datetime import datetime, timezone

from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Dataset(Base):

    __tablename__ = "datasets"

    __table_args__ = {
        "schema": "metadata"
    }

    # Primary Key
    dataset_id: Mapped[int] = mapped_column(
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

    # Physical Storage
    schema_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    table_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    # Dataset Characteristics
    data_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    geometry_type: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    crs: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    # Logical Schema Reference
    schema_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("metadata.dataset_schemas.schema_id"),
        nullable=True
    )

    # Dataset Status
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="draft"
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    dataset_schema = relationship(
        "DatasetSchema",
        back_populates="datasets"
    )

    sources = relationship(
        "DatasetSource",
        back_populates="dataset"
    )

    ingestion_jobs = relationship(
        "IngestionJob",
        back_populates='dataset'
    )