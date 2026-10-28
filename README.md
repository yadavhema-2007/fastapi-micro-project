# FastAPI Development, Automated Testing, and GitHub Workflow

Welcome to the **FastAPI Micro Project** repository. This project demonstrates backend web development using **FastAPI**, **Pydantic v2**, **Uvicorn**, and **pytest**, accompanied by a software engineering **GitHub Workflow** (Issue $\rightarrow$ Branch $\rightarrow$ Code $\rightarrow$ Commit $\rightarrow$ PR).

---

## 📑 Table of Contents

1. [Project Overview & Architecture](#-project-overview--architecture)
2. [Prerequisites & Environment Setup](#-prerequisites--environment-setup)
3. [Project 1: Basic Greeting & Health API](#-project-1-basic-greeting--health-api)
4. [Project 2: Task Management CRUD API](#-project-2-task-management-crud-api)
5. [Automated Testing Suite (23 Passed)](#-automated-testing-suite-23-passed)
6. [Git Workflow Demonstration (States A–F)](#-git-workflow-demonstration-states-af)
7. [Instructor Presentation & Oral Defense Guide](#-instructor-presentation--oral-defense-guide)
8. [Final Task Checklist](#-final-task-checklist)

---

## 🏛️ Project Overview & Architecture

```text
fastapi-micro-project-antigravity/
│
├── .gitignore                      # Excludes .venv, __pycache__, .pytest_cache
├── .venv/                          # Python 3.15.1 virtual environment
├── README.md                       # Master documentation (this file)
│
├── project1_basic/                 # PROJECT 1: Basic Greeting & Health Check API
│   ├── main.py                     # Root (GET /) and Health (GET /health) endpoints
│   ├── test_main.py                # 5 passing automated pytest test cases
│   ├── requirements.txt            # Package dependencies
│   └── README.md                   # Dedicated setup and usage guide
│
└── project2_crud/                  # PROJECT 2: Task Management CRUD API
    ├── main.py                     # CRUD routes and Pydantic validation schemas
    ├── test_main.py                # 18 passing automated pytest test cases
    ├── requirements.txt            # Package dependencies
    └── README.md                   # Dedicated setup and API testing guide
```

---

## ⚙️ Prerequisites & Environment Setup

- **Python**: 3.10+ (Verified on Python 3.15.1 64-bit)
- **Git**: 2.40+ (Verified on Git 2.55.0)
- **OS**: Windows (PowerShell commands provided)

### Setup Steps:
```powershell
# 1. Clone or navigate to the workspace
cd "c:\Users\SHREYAS REDDY\OneDrive\Desktop\fastapi-micro-project-antigravity"

# 2. Create the Python virtual environment
python -m venv .venv

# 3. Activate the virtual environment
.\.venv\Scripts\Activate.ps1
# If PowerShell blocks script execution, run:
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 4. Install dependencies for Project 1 or Project 2
pip install -r project1_basic/requirements.txt
```

---

## 🚀 Project 1: Basic Greeting & Health API

### Endpoints
- `GET /` — Returns `{"message": "Welcome to the FastAPI Micro Project!"}`
- `GET /health` — Returns `{"status": "ok"}`
- `GET /docs` — Interactive Swagger UI
- `GET /redoc` — Alternative ReDoc specification

### Running Project 1
```powershell
cd project1_basic
uvicorn main:app --reload --port 8000
```
Open in browser:
- [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Testing Project 1
```powershell
cd project1_basic
python -m pytest -v
```
**Result**: 5 passed in 0.48s.

---

## 📋 Project 2: Task Management CRUD API

### Endpoints & Status Codes
| Method | Path | Status Code | Purpose |
| :--- | :--- | :--- | :--- |
| **POST** | `/tasks` | `201 Created` | Create a task (validates input) |
| **GET** | `/tasks` | `200 OK` | List all tasks |
| **GET** | `/tasks/{task_id}` | `200 OK` / `404 Not Found` | Retrieve a single task by ID |
| **PUT** | `/tasks/{task_id}` | `200 OK` / `404 Not Found` | Update fields of an existing task |
| **DELETE** | `/tasks/{task_id}` | `204 No Content` / `404 Not Found`| Delete a task (no response body) |

### In-Memory Storage Note
Tasks are stored inside an in-memory dictionary (`tasks_db`). Data resides strictly in RAM. When the Uvicorn process restarts, data is reset. In production, this layer is replaced by an ORM (SQLAlchemy/SQLModel) connected to PostgreSQL or SQLite.

### Running Project 2
```powershell
cd project2_crud
uvicorn main:app --reload --port 8000
```
Open interactive documentation: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Testing Project 2
```powershell
cd project2_crud
python -m pytest -v
```
**Result**: 18 passed in 0.65s.

---

## 🧪 Automated Testing Suite (23 Passed)

### Project 1: 5 Tests Passed
```text
test_main.py::test_read_root_status_code PASSED                          [ 20%]
test_main.py::test_read_root_json_content PASSED                         [ 40%]
test_main.py::test_health_check_status_code PASSED                       [ 60%]
test_main.py::test_health_check_json_content PASSED                      [ 80%]
test_main.py::test_nonexistent_route_returns_404 PASSED                  [100%]
======================== 5 passed in 0.48s =========================
```

### Project 2: 18 Tests Passed
```text
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
======================== 18 passed in 0.65s ========================
```

---

## 🌿 Git Workflow Demonstration (States A–F)

This project demonstrates the complete engineering workflow using real Git commits:

| State | Git Command | Meaning / Description |
| :--- | :--- | :--- |
| **State A: Clean Branch** | `git checkout -b feature/health-check` | New branch pointer isolated from `main`. Clean working tree. |
| **State B: Uncommitted Changes** | `git status`, `git diff` | Code edits exist only in local working directory on disk. |
| **State C: Staged Changes** | `git add project1_basic/` | Changes staged into Git Index, ready for commit packaging. |
| **State D: Committed Locally** | `git commit -m "Add health check endpoint"` | Permanent snapshot created in local repository (`00a2a11`). |
| **State E: Pushed to Remote** | `git push -u origin feature/health-check` | Commits transmitted to remote upstream repository. |
| **State F: Pull Request** | Open PR on GitHub | Code submitted for review and automated CI verification. |

### Pull Request Submission Template
- **Title**: `Add health-check endpoint`
- **Description**:
  ```markdown
  ## Summary of Changes
  - Added `GET /health` returning `{"status": "ok"}` for uptime monitoring.
  - Added automated tests in `test_main.py` asserting status code 200 and JSON structure.

  ## Automated Test Verification
  - Ran `python -m pytest -v`: 5 passed in 0.48s.

  Closes #1
  ```

---

## 🎓 Instructor Presentation & Oral Defense Guide

When demonstrating this project to your instructor, highlight these key design points:

1. **Why FastAPI over Flask or Django?**
   - FastAPI is asynchronous (ASGI), achieving NodeJS/Go performance.
   - Built-in type safety and automatic interactive Swagger documentation (`/docs`) out of the box.
2. **Why Pydantic Models instead of raw dictionaries?**
   - Pydantic validates data schemas, types, and constraints before endpoint code executes. Bad requests are rejected with HTTP `422 Unprocessable Entity` automatically.
3. **Why HTTP 204 for DELETE?**
   - RFC 9110 specifies HTTP 204 No Content for successful operations that intentionally return an empty body, saving bandwidth.
4. **How are test side-effects prevented?**
   - In `project2_crud/test_main.py`, a `@pytest.fixture(autouse=True)` calls `reset_db()` before and after every test, ensuring complete data isolation.

---

## ✅ Final Task Checklist

- [x] Python virtual environment (`.venv`) created and verified
- [x] Project 1 built with `GET /`, `GET /health`, and Swagger docs
- [x] Project 1 automated tests executed and verified (**5 passed**)
- [x] Project 2 built with CRUD operations and Pydantic validation
- [x] Project 2 automated tests executed and verified (**18 passed**)
- [x] In-memory storage and persistence caveats explained
- [x] Git workflow demonstrated through States A, B, C, D, E, and F
- [x] Dedicated READMEs created for both projects and repository root
- [x] Presentation defense guide and code walkthrough completed
