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


class IngestionJob(Base):

    __tablename__ = "ingestion_jobs"

    __table_args__ = {
        "schema": "metadata"
    }

    # Primary Key
    job_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # References
    dataset_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("metadata.datasets.dataset_id"),
        nullable=True
    )

    source_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("metadata.dataset_sources.source_id"),
        nullable=True
    )

    # Operation Information
    operation_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pending"
    )

    # Timestamps
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    # Processing Statistics
    records_detected: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    records_inserted: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    records_updated: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    records_deleted: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    records_rejected: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    # Error Information
    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # Relationships
    dataset = relationship(
        "Dataset",
        back_populates="ingestion_jobs"
    )

    source = relationship(
        "DatasetSource",
        back_populates="ingestion_jobs"
    )

    transformations = relationship(
        "TransformationHistory",
        back_populates="ingestion_job"
    )