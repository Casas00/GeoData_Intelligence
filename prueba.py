from app.database.connection import SessionLocal
from app.models.dataset_schema import DatasetSchema

from app.services.dataset_schema_service import (
    get_available_schema_code
)


db = SessionLocal()

try:
    # Insert temporary records to simulate collisions

    test_records = [
        "HYDRO001",
        "HYDHY001",
        "HYD01001"
    ]

    for index, code in enumerate(test_records):
        db.add(
            DatasetSchema(
                schema_code=code,
                name=f"Test Schema {index}",
                description="Temporary test record",
                version=1,
                definition={
                    "fields": [],
                    "geometry": None
                }
            )
        )

    # Make temporary records visible to queries
    db.flush()

    # Search for an available code
    result = get_available_schema_code(
        db=db,
        name="Hydrography",
        version=1
    )

    print("Available schema code:", result)

finally:
    # Undo all temporary database changes
    db.rollback()
    db.close()
