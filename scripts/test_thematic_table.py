
import json

from pathlib import Path
from sqlalchemy import text

from app.database.connection import SessionLocal
from app.schemas.dataset_definition import DatasetDefinition
from app.services.thematic_table_service import create_thematic_table


# --------------------------------------------------
# Load dataset definitions
# --------------------------------------------------

def load_definition(filename: str) -> DatasetDefinition:

    file_path = Path("data/test_models") / filename

    with file_path.open("r", encoding="utf-8") as file:
        raw_definition = json.load(file)

    return DatasetDefinition.model_validate(raw_definition)


# --------------------------------------------------
# Verify table structure
# --------------------------------------------------

def verify_table(db, schema_name: str, table_name: str):

    result = db.execute(
        text("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = :schema_name
              AND table_name = :table_name
            ORDER BY ordinal_position
        """),
        {
            "schema_name": schema_name,
            "table_name": table_name
        }
    ).fetchall()

    if not result:
        raise AssertionError(f"Table {schema_name}.{table_name} was not created.")

    print(f"\nTable: {schema_name}.{table_name}")

    for column in result:
        print(
            f"  {column.column_name}: "
            f"{column.data_type} "
            f"(nullable: {column.is_nullable})"
        )

    return {column.column_name for column in result}


# --------------------------------------------------
# Main test
# --------------------------------------------------

def test_create_thematic_tables():

    schema_name = "test_thematic"

    vector_definition = load_definition("vector_building.json")
    tabular_definition = load_definition("tabular_population.json")

    db = SessionLocal()

    try:

        # Start transaction
        db.begin()

        # ------------------------------------------
        # 1. Create vector table
        # ------------------------------------------

        print("\nCreating vector table...")

        create_thematic_table(
            db=db,
            definition=vector_definition,
            schema_name=schema_name,
            table_name="buildings",
            data_type="vector"
        )

        vector_columns = verify_table(
            db, schema_name, "buildings"
        )

        assert "id" in vector_columns
        assert "geom" in vector_columns

        # Verify geometry type and SRID
        geometry_info = db.execute(
            text("""
                SELECT type, srid
                FROM geometry_columns
                WHERE f_table_schema = :schema_name
                  AND f_table_name = :table_name
                  AND f_geometry_column = 'geom'
            """),
            {
                "schema_name": schema_name,
                "table_name": "buildings"
            }
        ).first()

        assert geometry_info is not None
        assert geometry_info.type.upper() == "POLYGON"
        assert geometry_info.srid == 25831

        print("\nGeometry:")
        print(f"  Type: {geometry_info.type}")
        print(f"  SRID: {geometry_info.srid}")

        # Verify GiST index
        gist_index = db.execute(
            text("""
                SELECT indexname, indexdef
                FROM pg_indexes
                WHERE schemaname = :schema_name
                  AND tablename = :table_name
                  AND indexdef ILIKE '%USING gist%'
            """),
            {
                "schema_name": schema_name,
                "table_name": "buildings"
            }
        ).first()

        assert gist_index is not None

        print("\nSpatial index:")
        print(f"  {gist_index.indexname}")
        print(f"  {gist_index.indexdef}")


        # ------------------------------------------
        # 2. Create tabular table
        # ------------------------------------------

        print("\nCreating tabular table...")

        create_thematic_table(
            db=db,
            definition=tabular_definition,
            schema_name=schema_name,
            table_name="population",
            data_type="tabular"
        )

        tabular_columns = verify_table(
            db, schema_name, "population"
        )

        assert "id" in tabular_columns
        assert "geom" not in tabular_columns

        print("\nTabular structure verified.")


        # ------------------------------------------
        # 3. Finish tests
        # ------------------------------------------

        print("\nAll tests passed!")

    except Exception as e:

        print(f"\nTEST ERROR: {e}")
        raise

    finally:

        # Undo all test database changes
        db.rollback()
        db.close()

        print("\nTest transaction rolled back.")


if __name__ == "__main__":
    test_create_thematic_tables()
