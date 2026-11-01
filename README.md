# FastAPI Micro Projects & Git Workflow Master Suite

A comprehensive, production-grade micro project repository demonstrating **FastAPI backend development**, **Pydantic schema validation**, **automated testing with pytest and TestClient**, and **professional Git/GitHub development workflows**.

---

## 📁 Repository Architecture

```
fastapi_micro_project/
│── .github/
│   └── workflows/
│       └── ci.yml               # Automated GitHub Actions CI testing pipeline
│── project1_basic/
│   ├── main.py                  # Basic greeting & health-check API
│   ├── test_main.py             # pytest suite (3 test cases)
│   ├── requirements.txt         # Project 1 dependencies
│   └── README.md                # Project 1 documentation
│── project2_crud/
│   ├── main.py                  # Task Management CRUD API with Pydantic validation
│   ├── test_main.py             # pytest suite with data isolation fixture (15 test cases)
│   ├── requirements.txt         # Project 2 dependencies
│   └── README.md                # Project 2 documentation
│── .gitignore                   # Ignores .venv, caches, and bytecode
│── demo_runner.ps1              # Interactive CLI controller for instructor demo
│── GIT_WORKFLOW.md              # Complete guide to Git States A–F & Pull Request
│── INSTRUCTOR_DEMO_GUIDE.md     # Code explanations, concepts, and defense answers
└── README.md                    # Root repository documentation
```

---

## ⚡ Quick Start (Windows PowerShell)

### 1. Automated Interactive Demo (Recommended)
Run the built-in demo menu to run tests, start servers, or inspect Git history with a single keystroke:
```powershell
.\demo_runner.ps1
```

### 2. Manual Commands

#### Run All Automated Tests
- **Project 1:**
  ```powershell
  cd project1_basic
  ..\.venv\Scripts\python.exe -m pytest -v
  ```
- **Project 2:**
  ```powershell
  cd project2_crud
  ..\.venv\Scripts\python.exe -m pytest -v
  ```

#### Start Local Development Servers
- **Project 1 Server (Port 8000):**
  ```powershell
  cd project1_basic
  ..\.venv\Scripts\uvicorn.exe main:app --reload --port 8000
  ```
  - API Root: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
  - Health Check: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
  - Interactive Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

- **Project 2 Server (Port 8001):**
  ```powershell
  cd project2_crud
  ..\.venv\Scripts\uvicorn.exe main:app --reload --port 8001
  ```
  - Tasks API: [http://127.0.0.1:8001/tasks](http://127.0.0.1:8001/tasks)
  - Interactive Swagger Docs: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

---

## 📊 Endpoints Summary

### Project 1: Basic Greeting API
| Method | Endpoint | Status | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | `200 OK` | Returns welcome message |
| `GET` | `/health` | `200 OK` | Returns operational health status `{"status": "ok"}` |
| `GET` | `/docs` | `200 OK` | Interactive Swagger UI API documentation |

### Project 2: Task Management CRUD API
| Method | Endpoint | Status | Description | Request Body |
| :--- | :--- | :--- | :--- | :--- |
| `GET` | `/` | `200 OK` | API introduction & documentation link | None |
| `POST` | `/tasks` | `201 Created` | Create new task record | `{"title": "string", "completed": false}` |
| `GET` | `/tasks` | `200 OK` | List all tasks | None |
| `GET` | `/tasks/{id}` | `200 OK` / `404` | Retrieve specific task by ID | None |
| `PUT` | `/tasks/{id}` | `200 OK` / `404` | Update title or completed status | `{"title": "new text", "completed": true}` |
| `DELETE` | `/tasks/{id}` | `204 No Content` | Remove task record | None |
| `GET` | `/docs` | `200 OK` | Interactive Swagger UI API documentation | None |

---

## 🧪 Automated Testing Verification

Both projects feature 100% test pass rates using `pytest` and `fastapi.testclient.TestClient`:
- **Project 1:** 3/3 tests passing (`test_read_root`, `test_health_check`, `test_nonexistent_route`).
- **Project 2:** 15/15 tests passing, including empty database checks, creation, retrieval, updates, deletions, and negative boundary validation (empty title, whitespace title, missing fields).
- **Test Isolation:** Automatic `@pytest.fixture(autouse=True)` clears memory between each test to ensure tests never pollute one another.

---

## 🌿 Git Branches & History

```
* 2a2b9e3 (HEAD -> feature/health-check) Update demo runner test suite paths
* ee3a0e4 Add health check endpoint
* e7d0965 (main) Add GitHub Actions CI pipeline and demo runner script
* 1ba2a0f Add project2 CRUD API with Pydantic validation
* 84f3039 Initial commit: Add project1 basic greeting API
```

See [GIT_WORKFLOW.md](GIT_WORKFLOW.md) for full state transition analysis and [INSTRUCTOR_DEMO_GUIDE.md](INSTRUCTOR_DEMO_GUIDE.md) for the presentation guide.
