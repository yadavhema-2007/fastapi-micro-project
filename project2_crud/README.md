# Project 2: Task Management CRUD API with Pydantic Validation

A complete, beginner-friendly **FastAPI** micro-project demonstrating how to build a RESTful CRUD (Create, Read, Update, Delete) API with robust request data validation powered by **Pydantic**.

---

## 📌 Architecture & Design Decisions

### 1. In-Memory Data Storage
- Tasks are stored inside an in-memory Python dictionary (`tasks_db`).
- **Persistence Warning**: Data lives strictly inside process RAM. When the Uvicorn server restarts or shuts down, all stored data is cleared.
- In production architectures, this layer is replaced with an Object-Relational Mapper (ORM) such as **SQLAlchemy** or **SQLModel** connecting to PostgreSQL or SQLite.

### 2. Request & Response Separation (Pydantic Models)
- `TaskCreate`: Validates input when creating a task (rejects empty or whitespace titles).
- `TaskUpdate`: Allows partial or full updates (title, completed).
- `TaskResponse`: Defines the public schema returned to clients (guarantees `id`, `title`, and `completed`).

---

## 📁 Project Structure

```text
project2_crud/
│
├── main.py              # Application entrypoint, Pydantic schemas, and CRUD routes
├── test_main.py         # Comprehensive test suite (18 automated tests)
├── requirements.txt     # Python dependency declarations
└── README.md            # Project documentation and API reference
```

---

## 🛣️ API Endpoints Summary

| HTTP Method | Path | Status Code | Description |
| :--- | :--- | :--- | :--- |
| **POST** | `/tasks` | `201 Created` | Create a new task (validates payload) |
| **GET** | `/tasks` | `200 OK` | List all existing tasks |
| **GET** | `/tasks/{task_id}` | `200 OK` / `404 Not Found` | Retrieve a single task by ID |
| **PUT** | `/tasks/{task_id}` | `200 OK` / `404 Not Found` | Update fields of an existing task |
| **DELETE** | `/tasks/{task_id}` | `204 No Content` / `404 Not Found` | Delete a task (no response body) |

---

## ⚙️ Environment Setup & Installation

### 1. Navigate to the project folder:
```powershell
cd project2_crud
```

### 2. Activate your virtual environment:
```powershell
..\.venv\Scripts\Activate.ps1
```

### 3. Install required dependencies:
```powershell
pip install -r requirements.txt
```

---

## 🏃 Running the Application

Start Uvicorn with hot reloading on port 8000:

```powershell
uvicorn main:app --reload --port 8000
```

---

## 🌐 Manual API Testing with PowerShell / cURL

### 1. Create a Task (POST /tasks)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/tasks" -Method Post -ContentType "application/json" -Body '{"title": "Buy groceries", "completed": false}'
```
**Response (201 Created)**:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "completed": false
}
```

### 2. Test Validation Rejection (Empty Title)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/tasks" -Method Post -ContentType "application/json" -Body '{"title": "   "}'
```
**Response (422 Unprocessable Entity)**:
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "title"],
      "msg": "Value error, Task title cannot be empty or whitespace-only."
    }
  ]
}
```

### 3. List All Tasks (GET /tasks)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/tasks" -Method Get
```

### 4. Retrieve a Specific Task (GET /tasks/1)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/tasks/1" -Method Get
```

### 5. Update a Task (PUT /tasks/1)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/tasks/1" -Method Put -ContentType "application/json" -Body '{"completed": true}'
```

### 6. Delete a Task (DELETE /tasks/1)
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/tasks/1" -Method Delete
```
**Status Code**: `204 No Content`

### 7. Interactive Swagger Documentation
Open in browser:
```text
http://127.0.0.1:8000/docs
```

---

## 🧪 Running Automated Tests

Run all 18 automated tests in verbose mode:

```powershell
python -m pytest -v
```

### Expected Output:
```text
============================= test session starts =============================
platform win32 -- Python 3.15.1, pytest-9.1.1, pluggy-1.7.0
rootdir: ...\project2_crud
collected 18 items

test_main.py::test_list_tasks_empty PASSED                               [  5%]
test_main.py::test_list_tasks_populated PASSED                           [ 11%]
test_main.py::test_create_task_success PASSED                            [ 16%]
test_main.py::test_create_task_default_completed_flag PASSED             [ 22%]
test_main.py::test_create_task_validation_missing_title PASSED           [ 27%]
test_main.py::test_create_task_validation_empty_string_title PASSED      [ 33%]
test_main.py::test_create_task_validation_whitespace_only_title PASSED   [ 38%]
test_main.py::test_create_task_validation_invalid_completed_type PASSED  [ 44%]
test_main.py::test_get_task_by_id_success PASSED                         [ 50%]
test_main.py::test_get_task_by_id_not_found PASSED                       [ 55%]
test_main.py::test_update_task_full PASSED                               [ 61%]
test_main.py::test_update_task_partial_title_only PASSED                 [ 66%]
test_main.py::test_update_task_partial_completed_only PASSED             [ 72%]
test_main.py::test_update_task_validation_empty_title PASSED             [ 77%]
test_main.py::test_update_task_validation_whitespace_title PASSED        [ 83%]
test_main.py::test_update_task_not_found PASSED                          [ 88%]
test_main.py::test_delete_task_success PASSED                            [ 94%]
test_main.py::test_delete_task_not_found PASSED                          [100%]

======================== 18 passed in 0.86s ========================
```
