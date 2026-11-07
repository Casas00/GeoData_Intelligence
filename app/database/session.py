from sqlalchemy.orm import Session
from app.database.connection import SessionLocal
from collections.abc import Generator

def get_db() -> Generator[Session, None,None]:
    db = SessionLocal()

    try: 
        yield db
    finally:
        db.close()