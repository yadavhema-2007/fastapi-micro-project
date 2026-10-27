"""
Automated tests for Project 1: Basic FastAPI Application
Using pytest and FastAPI TestClient (built on HTTPX)
"""

from fastapi.testclient import TestClient
from main import app

# Create a test client instance connected to our FastAPI app
client = TestClient(app)


def test_read_root_status_code():
    """
    Verify that GET / returns HTTP 200 OK.
    """
    response = client.get("/")
    assert response.status_code == 200


def test_read_root_json_content():
    """
    Verify that GET / returns the expected welcome JSON payload.
    """
    response = client.get("/")
    assert response.json() == {"message": "Welcome to the FastAPI Micro Project!"}


def test_health_check_status_code():
    """
    Verify that GET /health returns HTTP 200 OK.
    """
    response = client.get("/health")
    assert response.status_code == 200


def test_health_check_json_content():
    """
    Verify that GET /health returns {"status": "ok"}.
    """
    response = client.get("/health")
    assert response.json() == {"status": "ok"}



def test_nonexistent_route_returns_404():
    """
    Verify that requesting an undefined route returns HTTP 404 Not Found.
    """
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
