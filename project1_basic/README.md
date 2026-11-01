# Project 1: Basic FastAPI Application

A beginner-friendly FastAPI application demonstrating fundamental REST API principles, routing, and automated testing.

---

## 📌 Project Overview
This project illustrates:
- How to create a FastAPI web application instance.
- How to define HTTP GET endpoints using decorators (`@app.get()`).
- How FastAPI serializes Python dictionaries into standard JSON responses.
- How to write unit tests using `pytest` and `fastapi.testclient.TestClient`.
- How to start a local development server using `uvicorn`.

---

## 🗂️ File Structure
```
project1_basic/
│── main.py            # FastAPI application source code
│── test_main.py       # Automated test suite using pytest & TestClient
│── requirements.txt   # List of Python dependencies
└── README.md          # Setup and execution guide
```

---

## ⚙️ Installation & Setup

1. **Navigate to the project directory:**
   ```powershell
   cd C:\Users\yadav\.gemini\antigravity\scratch\fastapi_micro_project\project1_basic
   ```

2. **Activate the Virtual Environment:**
   ```powershell
   # If from project root:
   ..\.venv\Scripts\Activate.ps1
   ```
   *Alternative if PowerShell execution policy blocks scripts:*
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
   *Or call Python directly without activating:*
   ```powershell
   ..\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```

3. **Install Dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

---

## 🚀 Running the Development Server

Start the Uvicorn ASGI server with hot-reload enabled:
```powershell
uvicorn main:app --reload --port 8000
```
- Or using the virtual environment python directly:
```powershell
..\.venv\Scripts\uvicorn.exe main:app --reload --port 8000
```

Once running:
- **Root Endpoint:** Open http://127.0.0.1:8000/ in your browser or curl.
- **Health Check Endpoint:** Open http://127.0.0.1:8000/health
- **Interactive Swagger Documentation:** Open http://127.0.0.1:8000/docs
- **Alternative ReDoc Documentation:** Open http://127.0.0.1:8000/redoc

To stop the server, press `Ctrl + C` in your terminal.

---

## 🧪 Running Automated Tests

Run pytest with verbose output:
```powershell
python -m pytest -v
```
Or using the virtual environment executable directly:
```powershell
..\.venv\Scripts\python.exe -m pytest -v
```

All test cases will run against the in-memory client without needing a live network server.
