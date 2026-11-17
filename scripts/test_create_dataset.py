from app.database.connection import SessionLocal
from app.schemas.dataset import DatasetCreate
from app.services.dataset_service import create_dataset

def test_create_dataset():

    db = SessionLocal()

    try:
        dataset_data = DatasetCreate(
            name='Test Buildings',
            description = 'Test dataset for building footprints',

            schema_name='test_schema',
            table_name='test_buildings',

            data_type='vector',

            geometry_type='Polygon',
            crs='EPSG:25831',

            schema_id=5
        )

        dataset = create_dataset(db,dataset_data)

        if dataset is None:
            print('ERROR: The specified logical schema does not exists.')
            return

        print("Dataset successfully created!")
        print(f"Dataset ID: {dataset.dataset_id}")
        print(f"Name: {dataset.name}")
        print(f"Physical schema: {dataset.schema_name}")
        print(f"Physical table: {dataset.table_name}")
        print(f"Logical schema ID: {dataset.schema_id}")
        print(f"Data type: {dataset.data_type}")

    except Exception as e:
        print(f'ERROR creating dataset: {e}')


    finally:
        db.close()

if __name__ == '__main__':
    test_create_dataset()