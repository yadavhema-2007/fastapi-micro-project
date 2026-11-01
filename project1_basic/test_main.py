from fastapi.testclient import TestClient
from main import app

# Create a TestClient instance to simulate HTTP requests without running a live server
client = TestClient(app)

def test_read_root():
    """Verify that GET / returns HTTP 200 and the expected welcome JSON."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI Micro Project!"}

def test_health_check():
    """Verify that GET /health returns HTTP 200 and {'status': 'ok'}."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_nonexistent_route():
    """Verify that requesting an undefined route returns HTTP 404 Not Found."""
    response = client.get("/nonexistent-route")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
