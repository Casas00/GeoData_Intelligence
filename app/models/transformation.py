from datetime import datetime, timezone

from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey
)

from sqlalchemy.dialects.postgresql import JSONB

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class TransformationHistory(Base):

    __tablename__ = "transformation_history"

    __table_args__ = {
        "schema": "metadata"
    }

    # Primary Key
    transformation_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Ingestion Reference
    job_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("metadata.ingestion_jobs.job_id"),
        nullable=False
    )

    # Transformation Information
    transformation_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    parameters: Mapped[dict | None] = mapped_column(
        JSONB,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="pending"
    )

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationship
    ingestion_job = relationship(
        "IngestionJob",
        back_populates="transformations"
    )