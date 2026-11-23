
import pytest

from app.services.transformations.operations import (
    is_operation_compatible,
)


@pytest.mark.parametrize(
    "operation, source, target, expected",
    [
        ("cast_integer", "string", "integer", True),
        ("cast_float", "string", "float", True),
        ("parse_boolean", "string", "boolean", True),
        ("parse_date", "string", "date", True),
        ("parse_datetime", "string", "datetime", True),

        # Operaciones directas
        ("direct", "integer", "integer", True),
        ("direct", "string", "string", True),

        # Conversiones a string
        ("cast_string", "integer", "string", True),
        ("cast_string", "float", "string", True),
        ("cast_string", "date", "string", True),

        # Combinaciones incompatibles
        ("direct", "string", "integer", False),
        ("cast_integer", "string", "float", False),
        ("cast_float", "integer", "float", False),
        ("parse_date", "integer", "date", False),
        ("parse_datetime", "string", "date", False),
        ("cast_string", "integer", "float", False),
    ],
)
def test_operation_compatibility(
    operation,
    source,
    target,
    expected,
):
    result = is_operation_compatible(
        operation,
        source,
        target,
    )

    assert result is expected
