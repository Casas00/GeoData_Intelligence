
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator
)


class FieldDefinition(BaseModel):
    """Defines an attribute within a logical dataset schema."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=100)

    type: Literal[
        "integer",
        "float",
        "string",
        "boolean",
        "date",
        "datetime"
    ]

    description: str | None = None
    required: bool = False

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip().lower()

        if not value:
            raise ValueError("Field name cannot be empty")

        if not value.replace("_", "").isalnum():
            raise ValueError(
                "Field names must contain only letters, numbers and underscores"
            )

        if value[0].isdigit():
            raise ValueError("Field names cannot start with a number")

        return value


class GeometryDefinition(BaseModel):
    """Defines the spatial characteristics of a dataset."""

    model_config = ConfigDict(extra="forbid")

    type: Literal[
        "Point",
        "MultiPoint",
        "LineString",
        "MultiLineString",
        "Polygon",
        "MultiPolygon"
    ]

    crs: str = Field(min_length=1, max_length=50)
    nullable: bool = False


class DatasetDefinition(BaseModel):
    """Defines the logical structure of a dataset."""

    model_config = ConfigDict(extra="forbid")

    fields: list[FieldDefinition] = Field(default_factory=list)
    geometry: GeometryDefinition | None = None

    @model_validator(mode="after")
    def validate_unique_fields(self):
        names = [field.name for field in self.fields]

        if len(names) != len(set(names)):
            raise ValueError("Field names must be unique")

        return self
