from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    password: str = Field(..., min_length=6, max_length=100, description="Password (min 6 characters)")

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        trimmed = value.strip().lower()
        if not trimmed:
            raise ValueError("Username cannot be empty or whitespace.")
        return trimmed


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    username: str
    created_at: datetime


class ProtectedDataResponse(BaseModel):
    message: str
    authenticated_user: str
    secret_vault_code: str
