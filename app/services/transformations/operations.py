from typing import Literal

FieldType = Literal[
    'integer',
    'float',
    'string',
    'boolean',
    'date',
    'datetime',
]

TransformationOperations = Literal[
    'direct',
    'cast_integer',
    'cast_float',
    'parse_boolean',
    'parse_date',
    'parse_datetime',
    'cast_string',
]

OPERATION_COMPATIBILITY = {
    "cast_integer": ("string", "integer"),
    "cast_float": ("string", "float"),
    "parse_boolean": ("string", "boolean"),
    "parse_date": ("string", "date"),
    "parse_datetime": ("string", "datetime"),
}

def is_operation_compatible(
    operation: TransformationOperations,
    source_type: FieldType,
    target_type:FieldType,
) -> bool:

    if operation == 'direct':
        return source_type == target_type

    if operation == 'cast_string':
        return target_type == 'string'

    expected_types = OPERATION_COMPATIBILITY.get(operation)

    if expected_types is None:
        return False

    return (source_type,target_type) == expected_types