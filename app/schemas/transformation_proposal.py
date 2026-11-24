
from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.core.constants import DEFAULT_CRS

from app.services.transformations.operations import (
    FieldType,
    TransformationOperations,
    is_operation_compatible,
)


# --------------------------------------------------
# Geometry types and operations
# --------------------------------------------------

SourceGeometryType = Literal[
    "Point",
    "MultiPoint",
    "LineString",
    "MultiLineString",
    "Polygon",
    "MultiPolygon",
]

TargetGeometryType = Literal[
    "MultiPoint",
    "MultiLineString",
    "MultiPolygon",
]

GeometryOperation = Literal[
    "direct",
    "wrap",
]


# --------------------------------------------------
# Field mapping
# --------------------------------------------------

class FieldMapping(BaseModel):
    """Defines the transformation of an individual field."""

    source: str = Field(..., description="Source field name")
    target: str = Field(..., description="Target field name")

    source_type: FieldType
    target_type: FieldType

    operation: TransformationOperations = Field(
        ...,
        description="Identifier of the transformation operation",
    )

    model_config = ConfigDict(extra="forbid")

    @field_validator("source", "target")
    @classmethod
    def validate_field_names(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Field name cannot be empty")

        return value

    @model_validator(mode="after")
    def validate_operation_compatibility(self):
        if not is_operation_compatible(
            self.operation,
            self.source_type,
            self.target_type,
        ):
            raise ValueError(
                f"Operation '{self.operation}' is not compatible "
                f"with source type '{self.source_type}' and "
                f"target type '{self.target_type}'"
            )

        return self


class FieldMappings(BaseModel):
    """Defines all field mappings within a transformation proposal."""

    mappings: list[FieldMapping] = Field(default_factory=list)

    model_config = ConfigDict(extra="forbid")

    @model_validator(mode="after")
    def validate_unique_fields(self):
        sources = [mapping.source for mapping in self.mappings]
        targets = [mapping.target for mapping in self.mappings]

        if len(sources) != len(set(sources)):
            raise ValueError("Source fields must be unique")

        if len(targets) != len(set(targets)):
            raise ValueError("Target fields must be unique")

        return self


# --------------------------------------------------
# Geometry transformation
# --------------------------------------------------

class GeometryTransformation(BaseModel):
    """Defines the geometric transformation of a dataset."""

    model_config = ConfigDict(extra="forbid")

    source_type: SourceGeometryType
    source_crs: str = Field(min_length=1, max_length=50)

    target_type: TargetGeometryType
    target_crs: Literal["EPSG:4326"] = DEFAULT_CRS

    operation: GeometryOperation

    @model_validator(mode="after")
    def validate_operation_compatibility(self):

        compatible_types = {
            "direct": {
                ("MultiPoint", "MultiPoint"),
                ("MultiLineString", "MultiLineString"),
                ("MultiPolygon", "MultiPolygon"),
            },
            "wrap": {
                ("Point", "MultiPoint"),
                ("LineString", "MultiLineString"),
                ("Polygon", "MultiPolygon"),
            },
        }

        if (
            self.source_type,
            self.target_type,
        ) not in compatible_types[self.operation]:
            raise ValueError(
                f"Operation '{self.operation}' is not compatible "
                f"with source type '{self.source_type}' and "
                f"target type '{self.target_type}'"
            )

        return self


# --------------------------------------------------
# Transformation proposal
# --------------------------------------------------

class TransformationProposal(BaseModel):
    """Defines the complete transformation proposal for a dataset."""

    model_config = ConfigDict(extra="forbid")

    mappings: FieldMappings = Field(default_factory=FieldMappings)
    geometry: GeometryTransformation | None = None
