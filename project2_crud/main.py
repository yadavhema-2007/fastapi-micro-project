"""
Project 2: CRUD API with Pydantic Validation
A beginner-friendly Task Management REST API using FastAPI and Pydantic.

NOTE ON STORAGE:
This project uses an in-memory dictionary (`tasks_db`) for data storage.
In-memory storage lives strictly in RAM while the Python process runs.
Whenever the server restarts, reloads, or terminates, all stored tasks are lost.
In production systems, a persistent database such as PostgreSQL, MySQL, or SQLite is used.
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field, field_validator

# ---------------------------------------------------------
# FastAPI Application Instance
# ---------------------------------------------------------
app = FastAPI(
    title="Task Management CRUD API",
    description="A complete CRUD API demonstrating Pydantic validation, HTTP status codes, and error handling.",
    version="1.0.0",
)

# ---------------------------------------------------------
# In-Memory Database Simulation
# ---------------------------------------------------------
# A dictionary mapping integer task IDs to task records.
# Example: { 1: {"id": 1, "title": "Buy groceries", "completed": False} }
tasks_db: dict[int, dict] = {}
_id_counter: int = 0


def get_next_id() -> int:
    """Increment and return the next sequential task ID."""
    global _id_counter
    _id_counter += 1
    return _id_counter


def reset_db() -> None:
    """
    Clear all stored tasks and reset the ID counter to 0.
    Used between automated test cases to guarantee data isolation.
    """
    global _id_counter
    tasks_db.clear()
    _id_counter = 0


# ---------------------------------------------------------
# Pydantic Schemas / Models
# ---------------------------------------------------------
class TaskCreate(BaseModel):
    """
    Request model for creating a new task.
    Pydantic automatically validates that:
    1. 'title' is a string and has at least 1 character.
    2. 'title' is not blank or whitespace-only.
    3. 'completed' is an optional boolean defaulting to False.
    """
    title: str = Field(
        ...,
        min_length=1,
        description="The task description or title. Cannot be blank.",
        examples=["Complete FastAPI micro project"],
    )
    completed: bool = Field(
        default=False,
        description="Indicates whether the task is already completed.",
    )

    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, value: str) -> str:
        """Reject titles that are only whitespace."""
        stripped = value.strip()
        if not stripped:
            raise ValueError("Task title cannot be empty or whitespace-only.")
        return stripped


class TaskUpdate(BaseModel):
    """
    Request model for updating an existing task.
    All fields are optional, allowing partial or full updates.
    """
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        description="New task title. Cannot be blank if provided.",
        examples=["Updated task title"],
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Updated completion status.",
    )

    @field_validator("title")
    @classmethod
    def validate_title_not_empty(cls, value: Optional[str]) -> Optional[str]:
        """If title is supplied, ensure it is not only whitespace."""
        if value is not None:
            stripped = value.strip()
            if not stripped:
                raise ValueError("Task title cannot be empty or whitespace-only.")
            return stripped
        return value


class TaskResponse(BaseModel):
    """
    Response model representing the public view of a task.
    Ensures outgoing JSON data conforms strictly to this structure.
    """
    id: int = Field(..., description="Unique integer identifier for the task.")
    title: str = Field(..., description="The task title.")
    completed: bool = Field(..., description="Whether the task has been completed.")


# ---------------------------------------------------------
# API Endpoints (CRUD)
# ---------------------------------------------------------

@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
)
def create_task(task_input: TaskCreate):
    """
    Create a new task and store it in memory.
    - **HTTP Method**: POST
    - **Path**: /tasks
    - **Status Code**: 201 Created on success
    - **Validation**: Pydantic validates payload; returns 422 if invalid.
    """
    new_id = get_next_id()
    task_record = {
        "id": new_id,
        "title": task_input.title,
        "completed": task_input.completed,
    }
    tasks_db[new_id] = task_record
    return task_record


@app.get(
    "/tasks",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    summary="List all tasks",
)
def list_tasks():
    """
    Retrieve all tasks currently stored in memory.
    - **HTTP Method**: GET
    - **Path**: /tasks
    - **Status Code**: 200 OK
    - **Returns**: A list of tasks (empty list if no tasks exist).
    """
    return list(tasks_db.values())


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Retrieve a single task by ID",
)
def get_task(task_id: int):
    """
    Retrieve a single task by its unique ID.
    - **HTTP Method**: GET
    - **Path**: /tasks/{task_id}
    - **Status Code**: 200 OK if found, 404 Not Found if missing.
    """
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    return task


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    summary="Update an existing task",
)
def update_task(task_id: int, task_update: TaskUpdate):
    """
    Update fields of an existing task.
    - **HTTP Method**: PUT
    - **Path**: /tasks/{task_id}
    - **Status Code**: 200 OK on success, 404 Not Found if missing.
    """
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )

    # Apply updates if provided in request body
    if task_update.title is not None:
        task["title"] = task_update.title
    if task_update.completed is not None:
        task["completed"] = task_update.completed

    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task by ID",
)
def delete_task(task_id: int):
    """
    Delete a task by its unique ID.
    - **HTTP Method**: DELETE
    - **Path**: /tasks/{task_id}
    - **Status Code**: 204 No Content on success, 404 Not Found if missing.
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found",
        )
    del tasks_db[task_id]
    # HTTP 204 No Content must have an empty response body
    return Response(status_code=status.HTTP_204_NO_CONTENT)
