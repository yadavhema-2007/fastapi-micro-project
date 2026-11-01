import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import models
from database import Base, get_db
from main import app

# In-memory SQLite database specifically isolated for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """Dependency override providing an in-memory session per test request."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Apply FastAPI dependency override
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_and_teardown_db():
    """Recreates database tables before each test and drops them afterwards."""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


# ---------------------------------------------------------
# ROOT ROUTE TESTS
# ---------------------------------------------------------

def test_read_root():
    """Verify that root endpoint returns status 200 and SQLite metadata."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "SQLite" in data["database"]
    assert "survives server restarts" in data["persistence"]


# ---------------------------------------------------------
# CREATE TASK (POST /tasks) TESTS
# ---------------------------------------------------------

def test_create_task_success():
    """Verify creating a valid task persists to database with autoincremented ID."""
    payload = {"title": "Master SQLAlchemy", "completed": False}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Master SQLAlchemy"
    assert data["completed"] is False
    assert "created_at" in data


def test_create_task_default_completed():
    """Verify completed defaults to False in database when omitted."""
    payload = {"title": "Database Indexing"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    assert response.json()["completed"] is False


def test_create_task_rejects_empty_title():
    """Verify empty string title fails Pydantic validation with HTTP 422."""
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_create_task_rejects_whitespace_title():
    """Verify whitespace-only title fails Pydantic validation with HTTP 422."""
    response = client.post("/tasks", json={"title": "     "})
    assert response.status_code == 422


# ---------------------------------------------------------
# LIST TASKS (GET /tasks) TESTS
# ---------------------------------------------------------

def test_list_tasks_empty():
    """Verify empty database returns empty list."""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_populated():
    """Verify listing tasks returns rows persisted in SQLite."""
    client.post("/tasks", json={"title": "Task One"})
    client.post("/tasks", json={"title": "Task Two"})

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task One"
    assert data[1]["title"] == "Task Two"


# ---------------------------------------------------------
# RETRIEVE SINGLE TASK (GET /tasks/{id}) TESTS
# ---------------------------------------------------------

def test_get_task_success():
    """Verify retrieving a task by primary key."""
    create_res = client.post("/tasks", json={"title": "Persisted Item"})
    task_id = create_res.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Persisted Item"


def test_get_task_not_found():
    """Verify nonexistent ID returns HTTP 404."""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task with ID 999 not found."}


# ---------------------------------------------------------
# UPDATE TASK (PUT /tasks/{id}) TESTS
# ---------------------------------------------------------

def test_update_task_success():
    """Verify updating title and status updates database row."""
    create_res = client.post("/tasks", json={"title": "Initial", "completed": False})
    task_id = create_res.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": "Updated", "completed": True})
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated"
    assert data["completed"] is True


def test_update_task_not_found():
    """Verify updating nonexistent task returns HTTP 404."""
    response = client.put("/tasks/999", json={"title": "Does Not Exist"})
    assert response.status_code == 404


def test_update_task_rejects_empty_title():
    """Verify updating with empty string title returns HTTP 422."""
    create_res = client.post("/tasks", json={"title": "Valid"})
    task_id = create_res.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": ""})
    assert response.status_code == 422


# ---------------------------------------------------------
# DELETE TASK (DELETE /tasks/{id}) TESTS
# ---------------------------------------------------------

def test_delete_task_success():
    """Verify deleting a task returns HTTP 204 No Content."""
    create_res = client.post("/tasks", json={"title": "To Delete"})
    task_id = create_res.json()["id"]

    del_res = client.delete(f"/tasks/{task_id}")
    assert del_res.status_code == 204

    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == 404


def test_delete_task_not_found():
    """Verify deleting nonexistent task returns HTTP 404."""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
