from app.database.connection import engine
from app.database.base import Base

# Import all the models here so that they are registered with SQLAlchemy
from app import models

def create_tables():
    print("Creating database tables...")

    Base.metadata.create_all(bind=engine)

    print("Database tables created successfully.")

if __name__ == "__main__":
    create_tables()