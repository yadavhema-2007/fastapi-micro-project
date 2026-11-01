# FastAPI Micro Projects & Git Workflow Master Suite

A comprehensive, production-grade micro project repository demonstrating **FastAPI backend development**, **Pydantic schema validation**, **SQLAlchemy ORM database persistence**, **automated testing with pytest and TestClient**, and **professional Git/GitHub development workflows**.

---

## 📁 Repository Architecture

```
fastapi_micro_project/
│── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI running 33 automated tests
│── project1_basic/              # Project 1: Basic Greeting & Health API (Port 8000)
│   ├── main.py
│   ├── test_main.py             # 3 automated tests (Root, Health, 404)
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│── project2_crud/               # Project 2: In-Memory Task Management CRUD (Port 8001)
│   ├── main.py                  # Pydantic v2 validation + Web Dashboard
│   ├── test_main.py             # 16 automated tests with DB isolation fixture
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│── project3_database/           # Project 3: Persistent SQLite & SQLAlchemy API (Port 8002)
│   ├── database.py              # Engine, SessionLocal, Base & get_db dependency
│   ├── models.py                # SQLAlchemy ORM Task model
│   ├── schemas.py               # Pydantic v2 schemas
│   ├── crud.py                  # Database operations
│   ├── main.py                  # FastAPI dependency injection
│   ├── test_main.py             # 14 automated tests with in-memory DB overrides
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│── .dockerignore                # Docker ignore rules
│── .gitignore                   # Ignores .venv, caches, bytecode, and *.db files
│── docker-compose.yml           # Runs all 3 services simultaneously in containers
│── requests.http                # 17 ready-to-run REST Client requests
│── demo_runner.ps1              # Interactive CLI controller for instructor demo
│── CHECKLIST.md                 # Formal deliverables checklist (100% complete)
│── GIT_WORKFLOW.md              # Complete guide to Git States A–F & Pull Request
│── INSTRUCTOR_DEMO_GUIDE.md     # 5-min demo script, defense Q&A & code breakdown
└── README.md                    # Root repository documentation
```

---

## ⚡ Quick Start (Windows PowerShell)

### 1. Interactive Demo Runner (Recommended)
Run the built-in demo menu to run tests, start servers, or inspect Git history with a single keystroke:
```powershell
.\demo_runner.ps1
```

### 2. Manual Commands

#### Run All Automated Tests
- **Project 1:**
  ```powershell
  cd project1_basic; ..\.venv\Scripts\python.exe -m pytest -v
  ```
- **Project 2:**
  ```powershell
  cd project2_crud; ..\.venv\Scripts\python.exe -m pytest -v
  ```
- **Project 3:**
  ```powershell
  cd project3_database; ..\.venv\Scripts\python.exe -m pytest -v
  ```

#### Start Local Development Servers
- **Project 1 Server (Port 8000):**
  ```powershell
  cd project1_basic; ..\.venv\Scripts\uvicorn.exe main:app --reload --port 8000
  ```
  - Root: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
  - Health: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
  - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

- **Project 2 Server (Port 8001):**
  ```powershell
  cd project2_crud; ..\.venv\Scripts\uvicorn.exe main:app --reload --port 8001
  ```
  - Web Dashboard: [http://127.0.0.1:8001/dashboard](http://127.0.0.1:8001/dashboard)
  - Swagger UI: [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)

- **Project 3 Server (Port 8002):**
  ```powershell
  cd project3_database; ..\.venv\Scripts\uvicorn.exe main:app --reload --port 8002
  ```
  - Persistent SQLite Database: `tasks.db` on disk
  - Swagger UI: [http://127.0.0.1:8002/docs](http://127.0.0.1:8002/docs)

---

## 🧪 Automated Testing Verification

All 3 projects feature 100% test pass rates:
- **Project 1:** 3/3 tests passing.
- **Project 2:** 16/16 tests passing.
- **Project 3:** 14/14 tests passing.
- **Total: 33 automated tests passing green.**
