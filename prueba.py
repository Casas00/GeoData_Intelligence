from sqlalchemy import text

from app.database.connection import engine, SessionLocal


# Test 1: Direct connection
with engine.connect() as connection:

    result = connection.execute(
        text("SELECT version();")
    )

    print("PostgreSQL:")
    print(result.scalar())


# Test 2: PostGIS
with engine.connect() as connection:

    result = connection.execute(
        text("SELECT PostGIS_Full_Version();")
    )

    print("\nPostGIS:")
    print(result.scalar())


# Test 3: Session
db = SessionLocal()

try:

    result = db.execute(
        text("SELECT current_database();")
    )

    print("\nDatabase:")
    print(result.scalar())

finally:
    db.close()