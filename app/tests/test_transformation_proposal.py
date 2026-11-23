import pytest
from pydantic import ValidationError

from app.schemas.transformation_proposal import FieldMapping


@pytest.mark.parametrize(
    "operation, source_type, target_type",
    [
        ("direct", "integer", "integer"),
        ("cast_integer", "string", "integer"),
        ("cast_float", "string", "float"),
        ("parse_boolean", "string", "boolean"),
        ("parse_date", "string", "date"),
        ("parse_datetime", "string", "datetime"),
        ("cast_string", "integer", "string"),
    ],
)
def test_valid_field_mapping(operation, source_type, target_type):
    mapping = FieldMapping(
        source="population",
        target="inhabitants",
        source_type=source_type,
        target_type=target_type,
        operation=operation,
    )

    assert mapping.operation == operation


@pytest.mark.parametrize(
    "operation, source_type, target_type",
    [
        ("direct", "string", "integer"),
        ("cast_integer", "string", "float"),
        ("cast_float", "integer", "float"),
        ("parse_date", "integer", "date"),
        ("parse_datetime", "string", "date"),
        ("cast_string", "integer", "float"),
    ],
)
def test_invalid_field_mapping(operation, source_type, target_type):
    with pytest.raises(ValidationError):
        FieldMapping(
            source="population",
            target="inhabitants",
            source_type=source_type,
            target_type=target_type,
            operation=operation,
        )


def test_empty_source_field():
    with pytest.raises(ValidationError):
        FieldMapping(
            source=" ",
            target="inhabitants",
            source_type="integer",
            target_type="integer",
            operation="direct",
        )


def test_unknown_operation():
    with pytest.raises(ValidationError):
        FieldMapping(
            source="population",
            target="inhabitants",
            source_type="string",
            target_type="integer",
            operation="unknown_operation",
        )