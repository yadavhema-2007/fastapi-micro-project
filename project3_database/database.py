from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# SQLite disk database file path
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# connect_args={"check_same_thread": False} is required for SQLite with multi-threaded FastAPI
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Session factory for generating database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all SQLAlchemy ORM models
Base = declarative_base()


def get_db():
    """
    FastAPI dependency that provides an isolated database session per request.
    Ensures the session is cleanly closed even if an unhandled exception occurs.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
