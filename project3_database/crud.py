from sqlalchemy.orm import Session
import models
import schemas
from typing import List, Optional


def get_task(db: Session, task_id: int) -> Optional[models.Task]:
    """Retrieve a single task record by its primary key ID."""
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> List[models.Task]:
    """Retrieve multiple tasks with pagination support."""
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
    """Create a new task row and persist it to SQLite disk storage."""
    db_task = models.Task(title=task.title, completed=task.completed)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate) -> Optional[models.Task]:
    """Update title and/or completed status on an existing task row."""
    db_task = get_task(db, task_id)
    if not db_task:
        return None

    if task_update.title is not None:
        db_task.title = task_update.title
    if task_update.completed is not None:
        db_task.completed = task_update.completed

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """Delete a task row from the database."""
    db_task = get_task(db, task_id)
    if not db_task:
        return False
    db.delete(db_task)
    db.commit()
    return True
