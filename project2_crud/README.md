# Project 2: Task Management CRUD API with Pydantic Validation

A comprehensive, beginner-friendly RESTful API micro project built using **FastAPI** and **Pydantic**. This project demonstrates complete Create, Read, Update, and Delete (CRUD) operations, robust request validation, HTTP status codes, and automated test coverage.

---

## 📌 Project Overview

This project demonstrates core backend patterns:
1. **CRUD Operations:** Implementing endpoints to create, retrieve, update, and delete resource items.
2. **Pydantic Validation:** Strict request body validation ensuring titles are non-empty and types are correct before endpoint functions execute.
3. **HTTP Status Codes:** Proper status codes according to REST conventions (`200 OK`, `201 Created`, `204 No Content`, `404 Not Found`, and `422 Unprocessable Entity`).
4. **In-Memory Storage:** Demonstrating state handling in memory during the application lifecycle.
5. **Automated Testing:** 14 automated unit tests testing positive flows, validation boundaries, and edge cases.

---

## 🗂️ File Structure

```
project2_crud/
│── main.py            # FastAPI application, Pydantic schemas, and CRUD routes
│── test_main.py       # Comprehensive pytest suite (14 test cases)
│── requirements.txt   # Project dependencies
└── README.md          # Setup, API documentation, and testing guide
```

---

## 📊 Endpoints Reference

| HTTP Method | Route / Endpoint | Status Code | Description | Request Body |
| :--- | :--- | :--- | :--- | :--- |
| **GET** | `/` | `200 OK` | API Welcome message & docs link | None |
| **POST** | `/tasks` | `201 Created` | Create a new task | `{"title": "string", "completed": false}` |
| **GET** | `/tasks` | `200 OK` | List all tasks | None |
| **GET** | `/tasks/{task_id}` | `200 OK` | Retrieve one task by ID | None |
| **PUT** | `/tasks/{task_id}` | `200 OK` | Update task title and/or status | `{"title": "new string", "completed": true}` |
| **DELETE** | `/tasks/{task_id}` | `204 No Content`| Delete a task by ID | None |
| **GET** | `/docs` | `200 OK` | Interactive Swagger UI Documentation | None |
| **GET** | `/redoc` | `200 OK` | Alternative ReDoc Documentation | None |

### Error Status Codes
- **404 Not Found**: Returned when requesting, updating, or deleting a `task_id` that does not exist in memory.
- **422 Unprocessable Entity**: Returned automatically by FastAPI and Pydantic when the client provides invalid data types, an empty title, or a title consisting only of whitespace.

---

## 💾 In-Memory Storage Note

> [!NOTE]
> This application uses an in-memory Python dictionary (`tasks_db = {}`) to store tasks. This means:
> - Data persists as long as the application server is running.
> - **When the server stops or restarts, all data is cleared.**
> - For production systems, you replace the dictionary with a persistent database like PostgreSQL or SQLite using an ORM like SQLAlchemy or SQLModel.

---

## ⚙️ Installation & Setup

1. **Open PowerShell and navigate to the project folder:**
   ```powershell
   cd C:\Users\yadav\.gemini\antigravity\scratch\fastapi_micro_project\project2_crud
   ```

2. **Activate the Virtual Environment:**
   ```powershell
   ..\.venv\Scripts\Activate.ps1
   ```
   *Alternative if PowerShell execution policy blocks scripts:*
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   *Or invoke Python from the virtual environment directly:*
   ```powershell
   ..\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

---

## 🚀 Running the Development Server

Start the server using Uvicorn with automatic reload:
```powershell
uvicorn main:app --reload --port 8000
```
Or with direct virtual environment path:
```powershell
..\.venv\Scripts\uvicorn.exe main:app --reload --port 8000
```

Once started:
- **Interactive Documentation:** Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test endpoints directly in your browser.
- **Alternative Documentation:** Visit [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

To stop the server, press `Ctrl + C` in your terminal.

---

## 🧪 Running Automated Tests

Run the full pytest suite with verbose output:
```powershell
python -m pytest -v
```
Or directly via the virtual environment:
```powershell
..\.venv\Scripts\python.exe -m pytest -v
```

All 14 tests run in memory without requiring a live web server or external database.
