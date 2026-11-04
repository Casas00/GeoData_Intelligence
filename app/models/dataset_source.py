from datetime import datetime, timezone

from sqlalchemy import (
    Integer,
    String,
    Text,
    BigInteger,
    DateTime,
    ForeignKey
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class DatasetSource(Base):

    __tablename__ = "dataset_sources"

    __table_args__ = {
        "schema": "metadata"
    }

    # Primary Key
    source_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    # Dataset Reference
    dataset_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("metadata.datasets.dataset_id"),
        nullable=False
    )

    # Source Information
    source_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    source_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    source_format: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    source_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    # File Information
    file_path: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    file_size: Mapped[int | None] = mapped_column(
        BigInteger,
        nullable=True
    )

    file_hash: Mapped[str | None] = mapped_column(
        String(64),
        nullable=True
    )

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Relationships
    dataset = relationship(
        "Dataset",
        back_populates="sources"
    )

    ingestion_jobs = relationship(
        "IngestionJob",
        back_populates="source"
    )