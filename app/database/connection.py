from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name
)

#Validate database configuration
if not database_url:
    raise RuntimeError("DATABASE_URL is not configured. Please set the DATABASE_URL environment variable.")

#Database Engine
engine = create_engine(
    database_url,
    pool_pre_ping=True
)

#Database session factory
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)





