from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "postgresql+psycopg://postgres:Abhi%402733@localhost:5432/session1"

# Database connection
engine = create_engine(DATABASE_URL)

# Create database session
SessionLocal = sessionmaker(bind=engine)


# Dependency: Database session function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass