# backend/app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings  # Make sure this points to your DATABASE_URL

# SQLAlchemy engine configuration (sync version)
engine = create_engine(
    settings.DATABASE_URL,  # Example: postgresql://postgres:admin123@localhost/kindergarten_meals
    connect_args={"options": "-c timezone=UTC"},
    pool_pre_ping=True,
    echo=False  # Set to True if you want to see SQL queries in the console
)

# Session factory (sync)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all models
Base = declarative_base()

# Dependency for routes (FastAPI will inject this in each request)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
