from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    """Base schema defining common fields and validation rules."""
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
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Task title cannot be empty or blank whitespace.")
        return trimmed


class TaskCreate(TaskBase):
    """Schema expected when creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task with optional fields."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    completed: Optional[bool] = Field(default=None)

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
    """Schema returned to API clients, formatted from the SQLAlchemy ORM model."""
    id: int
    title: str
    completed: bool
    created_at: datetime

    # Pydantic v2 configuration to read from arbitrary objects (ORM mode)
    model_config = ConfigDict(from_attributes=True)
