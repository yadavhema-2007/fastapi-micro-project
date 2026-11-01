import pytest
from fastapi.testclient import TestClient
from main import app, reset_db

# Create test client instance
client = TestClient(app)


@pytest.fixture(autouse=True)
def run_before_and_after_each_test():
    """
    Automatic fixture executed before and after every individual test function.
    Resets in-memory storage so tests remain isolated and independent.
    """
    reset_db()
    yield
    reset_db()


# ---------------------------------------------------------
# ROOT ROUTE TESTS
# ---------------------------------------------------------

def test_read_root():
    """Verify that root endpoint returns status 200, docs link, and dashboard link."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Task Management API!",
        "documentation": "/docs",
        "dashboard": "/dashboard"
    }


def test_serve_dashboard():
    """Verify that /dashboard returns HTTP 200 and serves HTML."""
    response = client.get("/dashboard")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Task Management Studio" in response.text


# ---------------------------------------------------------
# CREATE TASK (POST /tasks) TESTS
# ---------------------------------------------------------

def test_create_task_success():
    """Verify creating a valid task returns HTTP 201 and populated data."""
    payload = {"title": "Learn FastAPI", "completed": False}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Learn FastAPI"
    assert data["completed"] is False


def test_create_task_default_completed():
    """Verify that 'completed' defaults to False when omitted in the payload."""
    payload = {"title": "Read documentation"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Read documentation"
    assert data["completed"] is False


def test_create_task_rejects_empty_title():
    """Verify that an empty string title fails Pydantic validation with HTTP 422."""
    payload = {"title": "", "completed": False}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_create_task_rejects_whitespace_title():
    """Verify that a title consisting only of spaces fails validation with HTTP 422."""
    payload = {"title": "    ", "completed": False}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


def test_create_task_rejects_missing_title():
    """Verify that omitting the required 'title' field fails validation with HTTP 422."""
    payload = {"completed": True}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data


# ---------------------------------------------------------
# LIST TASKS (GET /tasks) TESTS
# ---------------------------------------------------------

def test_list_tasks_empty():
    """Verify that listing tasks on an empty database returns an empty list."""
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_populated():
    """Verify that listing tasks returns all created tasks."""
    client.post("/tasks", json={"title": "Task One"})
    client.post("/tasks", json={"title": "Task Two"})

    response = client.get("/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task One"
    assert tasks[1]["title"] == "Task Two"


# ---------------------------------------------------------
# RETRIEVE SINGLE TASK (GET /tasks/{id}) TESTS
# ---------------------------------------------------------

def test_get_task_success():
    """Verify retrieving an existing task returns HTTP 200 and the matching task."""
    create_res = client.post("/tasks", json={"title": "Specific Task"})
    task_id = create_res.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Specific Task"
    assert response.json()["id"] == task_id


def test_get_task_not_found():
    """Verify requesting a nonexistent task ID returns HTTP 404."""
    response = client.get("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task with ID 999 not found."}


# ---------------------------------------------------------
# UPDATE TASK (PUT /tasks/{id}) TESTS
# ---------------------------------------------------------

def test_update_task_success():
    """Verify updating a task's title and status returns HTTP 200 and updated record."""
    create_res = client.post("/tasks", json={"title": "Old Title", "completed": False})
    task_id = create_res.json()["id"]

    update_payload = {"title": "Updated Title", "completed": True}
    response = client.put(f"/tasks/{task_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Title"
    assert data["completed"] is True


def test_update_task_not_found():
    """Verify updating a nonexistent task returns HTTP 404."""
    response = client.put("/tasks/999", json={"title": "Does Not Exist"})
    assert response.status_code == 404
    assert response.json() == {"detail": "Task with ID 999 not found."}


def test_update_task_rejects_empty_title():
    """Verify updating with an empty title fails validation with HTTP 422."""
    create_res = client.post("/tasks", json={"title": "Valid Initial Title"})
    task_id = create_res.json()["id"]

    response = client.put(f"/tasks/{task_id}", json={"title": ""})
    assert response.status_code == 422


# ---------------------------------------------------------
# DELETE TASK (DELETE /tasks/{id}) TESTS
# ---------------------------------------------------------

def test_delete_task_success():
    """Verify deleting an existing task returns HTTP 204 No Content."""
    create_res = client.post("/tasks", json={"title": "To Be Deleted"})
    task_id = create_res.json()["id"]

    # Delete the task
    delete_res = client.delete(f"/tasks/{task_id}")
    assert delete_res.status_code == 204
    assert delete_res.text == ""

    # Verify it can no longer be retrieved
    get_res = client.get(f"/tasks/{task_id}")
    assert get_res.status_code == 404


def test_delete_task_not_found():
    """Verify attempting to delete a nonexistent task returns HTTP 404."""
    response = client.delete("/tasks/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Task with ID 999 not found."}
