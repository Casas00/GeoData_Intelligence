from typing import Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.schemas.dataset_definition import FieldDefinition

from app.services.transformations.operations import (
    TransformationOperations,
    is_operation_compatible,
)

class FieldMapping(BaseModel):
    source: str = Field(..., description='Source field name')
    target: str = Field(..., description='Target field name')

    source_type: Literal[
        'integer','float','string','boolean','date','datetime'
    ]

    target_type: Literal[
        'integer','float','string','boolean','date','datetime'
    ]

    operation: TransformationOperations = Field(
        ...,
        description='Identifier of the trasnformation operation'
    )

    model_config = ConfigDict(extra='forbid')

    @field_validator('source','target')
    @classmethod
    def validate_field_names(cls,value:str) -> str:
        value = value.strip()

        if not value:
            raise ValueError('Field name cannot be empty')

        return value

    @model_validator(mode="after")
    def validate_operation_compatibility(self):
        if not is_operation_compatible(
            self.operation,
            self.source_type,
            self.target_type,
        ):
            raise ValueError(
                f"Operation '{self.operation}' is not compatible with "
                f"source type '{self.source_type}' and "
                f"target type '{self.target_type}'"
            )

        return self