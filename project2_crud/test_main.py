"""
Automated Test Suite for Project 2: CRUD API with Pydantic Validation
Using pytest and FastAPI TestClient.

Tests cover:
- CRUD operations (POST, GET, PUT, DELETE)
- Pydantic schema validation (empty titles, whitespace, invalid types)
- HTTP status codes (200, 201, 204, 404, 422)
- State isolation via autouse fixture resetting database between tests
"""

import pytest
from fastapi.testclient import TestClient
from main import app, reset_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def clear_database():
    """
    Autouse fixture that runs before and after each test function.
    Resets the in-memory database to ensure tests are completely isolated.
    """
    reset_db()
    yield
    reset_db()


# ---------------------------------------------------------
# Test Cases: List Tasks (GET /tasks)
# ---------------------------------------------------------

def test_list_tasks_empty():
    """Verify that GET /tasks returns an empty list when no tasks exist."""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_populated():
    """Verify that GET /tasks returns all created tasks."""
    client.post("/tasks", json={"title": "Task One"})
    client.post("/tasks", json={"title": "Task Two", "completed": True})

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Task One"
    assert data[0]["completed"] is False
    assert data[1]["title"] == "Task Two"
    assert data[1]["completed"] is True


# ---------------------------------------------------------
# Test Cases: Create Task (POST /tasks)
# ---------------------------------------------------------

def test_create_task_success():
    """Verify creating a valid task returns HTTP 201 Created and correct body."""
    payload = {"title": "Learn FastAPI Testing", "completed": False}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Learn FastAPI Testing"
    assert data["completed"] is False


def test_create_task_default_completed_flag():
    """Verify 'completed' defaults to False if omitted from payload."""
    response = client.post("/tasks", json={"title": "Write Unit Tests"})
    assert response.status_code == 201
    data = response.json()
    assert data["completed"] is False


def test_create_task_validation_missing_title():
    """Verify that sending a body without 'title' triggers HTTP 422 Unprocessable Entity."""
    response = client.post("/tasks", json={"completed": True})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_create_task_validation_empty_string_title():
    """Verify that an empty string title triggers HTTP 422."""
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_create_task_validation_whitespace_only_title():
    """Verify that whitespace-only title is rejected by custom Pydantic validator."""
    response = client.post("/tasks", json={"title": "     "})
    assert response.status_code == 422
    assert "detail" in response.json()


def test_create_task_validation_invalid_completed_type():
    """Verify that passing a non-boolean for 'completed' triggers HTTP 422."""
    response = client.post("/tasks", json={"title": "Valid title", "completed": "not_a_boolean"})
    assert response.status_code == 422


# ---------------------------------------------------------
# Test Cases: Retrieve Task (GET /tasks/{task_id})
# ---------------------------------------------------------

def test_get_task_by_id_success():
    """Verify retrieving an existing task returns HTTP 200 and the task object."""
    create_res = client.post("/tasks", json={"title": "Specific Task"})
    task_id = create_res.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Specific Task"


def test_get_task_by_id_not_found():
    """Verify retrieving a nonexistent task ID returns HTTP 404 Not Found."""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task with ID 999 not found"}


# ---------------------------------------------------------
# Test Cases: Update Task (PUT /tasks/{task_id})
# ---------------------------------------------------------

def test_update_task_full():
    """Verify updating both title and completed fields returns HTTP 200 with new data."""
    client.post("/tasks", json={"title": "Original Title", "completed": False})

    update_payload = {"title": "Updated Title", "completed": True}
    response = client.put("/tasks/1", json=update_payload)
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"
    assert response.json()["completed"] is True


def test_update_task_partial_title_only():
    """Verify updating only title preserves existing completion status."""
    client.post("/tasks", json={"title": "Initial Title", "completed": True})

    response = client.put("/tasks/1", json={"title": "New Title Only"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title Only"
    assert response.json()["completed"] is True


def test_update_task_partial_completed_only():
    """Verify updating only completed status preserves existing title."""
    client.post("/tasks", json={"title": "Keep This Title", "completed": False})

    response = client.put("/tasks/1", json={"completed": True})
    assert response.status_code == 200
    assert response.json()["title"] == "Keep This Title"
    assert response.json()["completed"] is True


def test_update_task_validation_empty_title():
    """Verify updating with empty string title is rejected with HTTP 422."""
    client.post("/tasks", json={"title": "Initial Title"})

    response = client.put("/tasks/1", json={"title": ""})
    assert response.status_code == 422


def test_update_task_validation_whitespace_title():
    """Verify updating with whitespace-only title is rejected with HTTP 422."""
    client.post("/tasks", json={"title": "Initial Title"})

    response = client.put("/tasks/1", json={"title": "   "})
    assert response.status_code == 422


def test_update_task_not_found():
    """Verify updating a nonexistent task returns HTTP 404."""
    response = client.put("/tasks/999", json={"title": "Ghost Task"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task with ID 999 not found"}


# ---------------------------------------------------------
# Test Cases: Delete Task (DELETE /tasks/{task_id})
# ---------------------------------------------------------

def test_delete_task_success():
    """Verify deleting an existing task returns HTTP 204 No Content with empty body."""
    client.post("/tasks", json={"title": "Task to delete"})

    response = client.delete("/tasks/1")
    assert response.status_code == 204
    assert response.content == b""

    # Confirm the task no longer exists
    get_res = client.get("/tasks/1")
    assert get_res.status_code == 404

    # Confirm list is now empty
    list_res = client.get("/tasks")
    assert list_res.json() == []


def test_delete_task_not_found():
    """Verify deleting a nonexistent task returns HTTP 404 Not Found."""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task with ID 999 not found"}
