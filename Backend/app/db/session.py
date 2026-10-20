from typing import Generator
from sqlalchemy import create_engine #type:ignore
from sqlalchemy.orm import sessionmaker, DeclarativeBase #type:ignore
from app.core.config import settings

# Initialize SQLAlchemy engine using configured PostgreSQL URI
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,  # Automatically check and reconnect dropped database connections
    pool_size=10,
    max_overflow=20,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy database models."""
    pass


def get_db() -> Generator:
    """FastAPI dependency that provides a transactional database session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()