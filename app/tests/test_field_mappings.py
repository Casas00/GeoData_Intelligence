import pytest
from pydantic import ValidationError

from app.schemas.transformation_proposal import (
    FieldMapping,
    FieldMappings,
)


def create_mapping(source, target):
    return FieldMapping(
        source=source,
        target=target,
        source_type='string',
        target_type='integer',
        operation='cast_integer',
    )


def test_valid_field_mappings():
    mappings = FieldMappings(
        mappings=[
            create_mapping('building_id', 'id'),
            create_mapping('floors', 'number_of_floors'),
            create_mapping('height', 'height_m'),
        ]
    )

    assert len(mappings.mappings) == 3


def test_duplicate_source_fields():
    with pytest.raises(ValidationError):
        FieldMappings(
            mappings=[
                create_mapping('building_id', 'id'),
                create_mapping('building_id', 'identifier'),
            ]
        )


def test_duplicate_target_fields():
    with pytest.raises(ValidationError):
        FieldMappings(
            mappings=[
                create_mapping('building_id', 'id'),
                create_mapping('identifier', 'id'),
            ]
        )