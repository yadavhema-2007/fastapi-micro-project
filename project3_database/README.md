# Project 3: Persistent Task Management API with SQLite & SQLAlchemy ORM

A production-grade RESTful API demonstrating **database persistence**, **SQLAlchemy ORM modeling**, **FastAPI Dependency Injection (`Depends(get_db)`)**, and **isolated in-memory database testing**.

---

## 📌 Project Overview

While Project 2 demonstrates fast in-memory caching where data is lost on server restart, **Project 3 solves the persistence challenge**:
1. **Disk Persistence:** All tasks are written to a local SQLite database file (`tasks.db`). Restarting the server preserves all created and updated tasks!
2. **SQLAlchemy ORM:** Relational mapping from Python objects to SQL tables with schema definitions.
3. **Dependency Injection:** Database connections are managed via FastAPI's `Depends(get_db)` generator, ensuring safe session opening and clean closing per request.
4. **Test Database Overrides:** Automated tests run against an isolated in-memory SQLite database (`sqlite:///:memory:`), keeping production data completely untouched during test runs.

---

## 🗂️ File Architecture

```
project3_database/
│── database.py        # SQLAlchemy engine, SessionLocal, Base, and get_db dependency
│── models.py          # SQLAlchemy ORM Task model mapped to SQL table
│── schemas.py         # Pydantic v2 validation models with ConfigDict(from_attributes=True)
│── crud.py            # Reusable database query functions (create, read, update, delete)
│── main.py            # FastAPI endpoints injecting the database session
│── test_main.py       # Automated pytest suite with dependency overrides
│── requirements.txt   # Dependencies
└── README.md          # Setup & architecture guide
```

---

## 🚀 Running the Development Server

Start the server using Uvicorn:
```powershell
uvicorn main:app --reload --port 8002
```
Or directly using the virtual environment:
```powershell
..\.venv\Scripts\uvicorn.exe main:app --reload --port 8002
```

Once started:
- **Interactive Swagger Documentation:** [http://127.0.0.1:8002/docs](http://127.0.0.1:8002/docs)
- **SQLite Database File:** Notice `tasks.db` automatically created on disk in the project folder.

---

## 🧪 Running Automated Tests

```powershell
python -m pytest -v
```
Or via virtualenv:
```powershell
..\.venv\Scripts\python.exe -m pytest -v
```
All tests execute using in-memory SQLite without modifying `tasks.db` on disk.
