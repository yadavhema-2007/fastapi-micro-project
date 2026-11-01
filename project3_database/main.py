from fastapi import FastAPI, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
import crud
from database import engine, get_db

# Create SQLite database tables on startup if they do not exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Persistent Task Management API (SQLite + SQLAlchemy)",
    description="Production-grade CRUD API with SQLite disk persistence and dependency injection.",
    version="1.0.0"
)


@app.get("/", tags=["General"])
def read_root():
    """Welcome route confirming persistent database connectivity."""
    return {
        "message": "Welcome to the SQLite Persistent Task Management API!",
        "database": "SQLite (tasks.db on disk)",
        "persistence": "Data survives server restarts",
        "documentation": "/docs"
    }


@app.post(
    "/tasks",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create task in SQLite database"
)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Creates a new task record in SQLite and returns the saved row with generated ID."""
    return crud.create_task(db=db, task=task_in)


@app.get(
    "/tasks",
    response_model=List[schemas.TaskResponse],
    status_code=status.HTTP_200_OK,
    tags=["Tasks"],
    summary="List tasks from SQLite"
)
def list_tasks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Retrieves all tasks stored in SQLite with pagination support."""
    return crud.get_tasks(db=db, skip=skip, limit=limit)


@app.get(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_200_OK,
    tags=["Tasks"],
    summary="Retrieve task by ID"
)
def get_task(task_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Retrieves a single task row or returns HTTP 404 if not found."""
    db_task = crud.get_task(db=db, task_id=task_id)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )
    return db_task


@app.put(
    "/tasks/{task_id}",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_200_OK,
    tags=["Tasks"],
    summary="Update task in SQLite"
)
def update_task(
    task_id: int = Path(..., ge=1),
    task_update: schemas.TaskUpdate = ...,
    db: Session = Depends(get_db)
):
    """Updates fields on an existing task row or returns HTTP 404."""
    db_task = crud.update_task(db=db, task_id=task_id, task_update=task_update)
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )
    return db_task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete task from SQLite"
)
def delete_task(task_id: int = Path(..., ge=1), db: Session = Depends(get_db)):
    """Deletes a task row or returns HTTP 404."""
    success = crud.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )
    return None
