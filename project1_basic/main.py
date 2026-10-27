"""
Project 1: Basic FastAPI Application
A beginner-friendly FastAPI application demonstrating fundamental REST API concepts.
"""

from fastapi import FastAPI

# Initialize the FastAPI application instance
app = FastAPI(
    title="Basic Greeting API",
    description="A beginner-friendly FastAPI service demonstrating root greeting and health check.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    """
    Root endpoint that returns a friendly welcome greeting.
    HTTP Method: GET
    Route: /
    Response: JSON object with a greeting message
    """
    return {"message": "Welcome to the FastAPI Micro Project!"}
