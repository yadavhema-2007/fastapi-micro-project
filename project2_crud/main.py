from fastapi import FastAPI, HTTPException, status, Path
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

# Initialize the FastAPI application
app = FastAPI(
    title="Task Management API",
    description="A complete CRUD API demonstrating Pydantic validation, status codes, and error handling.",
    version="1.0.0"
)

# ---------------------------------------------------------
# IN-MEMORY DATABASE
# ---------------------------------------------------------
# A Python dictionary stores task records in RAM during runtime.
# IMPORTANT: Data stored here is ephemeral and is wiped when the server restarts.
tasks_db: dict[int, dict] = {}
task_id_counter: int = 0


# ---------------------------------------------------------
# PYDANTIC SCHEMAS (DATA VALIDATION & SERIALIZATION)
# ---------------------------------------------------------

class TaskBase(BaseModel):
    """Base schema shared between create and response models."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Task title (cannot be empty, max 100 characters)"
    )
    completed: bool = Field(
        default=False,
        description="Whether the task has been finished"
    )

    @field_validator("title")
    @classmethod
    def validate_title_not_whitespace(cls, value: str) -> str:
        """Reject titles that are only whitespace characters."""
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Task title cannot be empty or blank whitespace.")
        return trimmed


class TaskCreate(TaskBase):
    """Schema expected in the request body when creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task. Fields are optional."""
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Updated task title"
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Updated task completion status"
    )

    @field_validator("title")
    @classmethod
    def validate_title_not_whitespace(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            trimmed = value.strip()
            if not trimmed:
                raise ValueError("Task title cannot be empty or blank whitespace.")
            return trimmed
        return value


class TaskResponse(BaseModel):
    """Schema returned to the client, including the server-generated task ID."""
    id: int = Field(..., description="Unique integer ID of the task")
    title: str = Field(..., description="Title of the task")
    completed: bool = Field(..., description="Completion status of the task")


def reset_db() -> None:
    """Helper function to clear database state (useful for automated testing)."""
    global tasks_db, task_id_counter
    tasks_db.clear()
    task_id_counter = 0


# ---------------------------------------------------------
# API ROUTES (ENDPOINTS)
# ---------------------------------------------------------

@app.get("/", tags=["General"])
def read_root():
    """Welcome route providing guidance to API consumers."""
    return {
        "message": "Welcome to the Task Management API!",
        "documentation": "/docs"
    }


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a new task"
)
def create_task(task_in: TaskCreate):
    """
    Create a new task in memory:
    - **title**: Non-empty text string
    - **completed**: Boolean flag (defaults to false)
    Returns HTTP 201 Created with the persisted task record.
    """
    global task_id_counter
    task_id_counter += 1
    new_task = {
        "id": task_id_counter,
        "title": task_in.title,
        "completed": task_in.completed,
    }
    tasks_db[task_id_counter] = new_task
    return new_task


@app.get(
    "/tasks",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    tags=["Tasks"],
    summary="List all tasks"
)
def list_tasks():
    """Retrieve all current tasks stored in memory."""
    return list(tasks_db.values())


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    tags=["Tasks"],
    summary="Get a specific task by ID"
)
def get_task(task_id: int = Path(..., ge=1, description="Unique positive ID of the task")):
    """
    Retrieve details of a single task by its integer identifier.
    Returns HTTP 404 if the task ID does not exist.
    """
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )
    return task


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    tags=["Tasks"],
    summary="Update an existing task"
)
def update_task(
    task_id: int = Path(..., ge=1, description="Unique positive ID of the task to update"),
    task_update: TaskUpdate = ...
):
    """
    Update fields of an existing task:
    - **title**: New title (optional)
    - **completed**: New boolean status (optional)
    Returns HTTP 404 if the task does not exist.
    """
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )

    if task_update.title is not None:
        task["title"] = task_update.title
    if task_update.completed is not None:
        task["completed"] = task_update.completed

    tasks_db[task_id] = task
    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete a task"
)
def delete_task(task_id: int = Path(..., ge=1, description="Unique positive ID of the task to delete")):
    """
    Delete a task from the in-memory database.
    Returns HTTP 204 No Content upon success, or HTTP 404 if the task was not found.
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )
    del tasks_db[task_id]
    return None
