from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from database import Base


class Task(Base):
    """SQLAlchemy ORM model mapped directly to the 'tasks' table in SQLite."""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
