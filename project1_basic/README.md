# Project 1: Basic FastAPI Application

A beginner-friendly introductory micro-project built with **FastAPI**, **Uvicorn**, and **pytest**. This project demonstrates fundamental backend web development concepts, including HTTP routing, JSON responses, health monitoring endpoints, and automated unit testing.

---

## 📁 Project Structure

```text
project1_basic/
│
├── main.py              # Application entrypoint with FastAPI routes
├── test_main.py         # Automated test suite using pytest and TestClient
├── requirements.txt     # Python dependency declarations
└── README.md            # Project documentation and usage guide
```

---

## 🚀 Key Features

- **Root Endpoint (`GET /`)**: Returns a welcome message greeting the API consumer.
- **Health-Check Endpoint (`GET /health`)**: Returns `{"status": "ok"}` for uptime monitoring and load balancers.
- **Automatic Interactive Docs (`/docs`)**: Interactive Swagger UI generated automatically by FastAPI.
- **Alternative Documentation (`/redoc`)**: Clean ReDoc specification.
- **Automated Test Suite (`test_main.py`)**: Tests HTTP status codes, JSON payload integrity, and 404 handling.

---

## ⚙️ Environment Setup & Installation

### 1. Navigate to the project directory:
```powershell
cd project1_basic
```

### 2. Activate the virtual environment:
If using the root virtual environment:
```powershell
..\.venv\Scripts\Activate.ps1
```
*(Or create a new one inside this folder via `python -m venv .venv` and activate it).*

### 3. Install required dependencies:
```powershell
pip install -r requirements.txt
```

---

## 🏃 Running the Application

Start the development server using **Uvicorn** with hot reloading enabled:

```powershell
uvicorn main:app --reload --port 8000
```

### Explanation of parameters:
- `main`: Refers to the Python file `main.py`.
- `app`: Refers to the `FastAPI()` instance created inside `main.py`.
- `--reload`: Automatically restarts the server whenever code changes are saved.
- `--port 8000`: Runs the application on port 8000.

---

## 🌐 Testing Endpoints

Once the server is running, you can test the endpoints in your browser, with `curl`, or using PowerShell:

### 1. Root Greeting
- **URL**: `http://127.0.0.1:8000/`
- **Method**: `GET`
- **Expected Response**:
  ```json
  {
    "message": "Welcome to the FastAPI Micro Project!"
  }
  ```

### 2. Health Check
- **URL**: `http://127.0.0.1:8000/health`
- **Method**: `GET`
- **Expected Response**:
  ```json
  {
    "status": "ok"
  }
  ```

### 3. Interactive Documentation
- **Swagger UI**: Open `http://127.0.0.1:8000/docs` in your browser.
- **ReDoc UI**: Open `http://127.0.0.1:8000/redoc` in your browser.

---

## 🧪 Running Automated Tests

Run the test suite using `pytest` in verbose mode:

```powershell
python -m pytest -v
```

### Expected Output:
```text
test_main.py::test_read_root_status_code PASSED                          [ 20%]
test_main.py::test_read_root_json_content PASSED                         [ 40%]
test_main.py::test_health_check_status_code PASSED                       [ 60%]
test_main.py::test_health_check_json_content PASSED                      [ 80%]
test_main.py::test_nonexistent_route_returns_404 PASSED                  [100%]

======================== 5 passed in 0.53s =========================
```
