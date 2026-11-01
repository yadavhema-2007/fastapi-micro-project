# Instructor Demonstration & Oral Defense Guide

This document is your preparation handbook for demonstrating the FastAPI Micro Projects to your instructor, professor, or technical interviewer.

---

## 🎤 5-Minute Live Demonstration Script

Follow this step-by-step sequence during your presentation:

### Minute 1: Introduction & Architecture
1. **Explain the Goal:**  
   *"I built two production-grade FastAPI applications demonstrating modern Python web patterns, automated testing with pytest and TestClient, Pydantic data validation, and Git branching workflows."*
2. **Show the Directory Structure:**  
   Show the repository in VS Code or File Explorer (`project1_basic`, `project2_crud`, `.github`, `demo_runner.ps1`).

### Minute 2: Automated Testing Demonstration
1. **Launch the Demo Controller:**
   ```powershell
   .\demo_runner.ps1
   ```
2. **Press `1`** to run all tests.
3. **Point out the Terminal Output:**
   - Show `project1_basic`: 3 passed.
   - Show `project2_crud`: 15 passed.
   - *"Notice how all 18 test cases run in under 2 seconds. Because we use FastAPI's `TestClient`, tests execute directly in memory without needing network sockets or slow server startups."*

### Minute 3: Project 1 Walkthrough (Routes & Status Codes)
1. In `demo_runner.ps1`, press **`4`** to start Project 1 on port 8000.
2. Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) in your browser.
3. Show the interactive Swagger UI:
   - Click `GET /` ➔ Click **Try it out** ➔ Click **Execute** ➔ Show HTTP 200 and JSON message.
   - Click `GET /health` ➔ Execute ➔ Show `{"status": "ok"}`.
4. Explain: *"FastAPI automatically reads our Python type hints and generates this OpenAPI documentation with zero extra documentation code."*

### Minute 4: Project 2 Walkthrough (Pydantic CRUD & Validation)
1. Stop Project 1 (`Ctrl + C`) and start Project 2 (press **`5`** in `demo_runner.ps1` or run `uvicorn main:app --port 8001` in `project2_crud`).
2. Open [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs).
3. **Show Successful Creation:**
   - Execute `POST /tasks` with `{"title": "Buy groceries", "completed": false}`.
   - Show response: HTTP `201 Created` with generated `id: 1`.
4. **Show Pydantic Validation Error (Crucial Defense Moment):**
   - Execute `POST /tasks` with `{"title": "   ", "completed": false}` (only whitespace).
   - Show response: HTTP `422 Unprocessable Entity` with error message *"Task title cannot be empty or blank whitespace."*
   - Explain: *"This proves that our custom Pydantic `@field_validator` stopped invalid input before it could ever pollute our storage."*

### Minute 5: Git Workflow & Pull Request Defense
1. Stop the server, return to `demo_runner.ps1`, and press **`6`** (Git graph) and **`7`** (Git diff).
2. Show the Git tree:
   ```text
   * ee3a0e4 (HEAD -> feature/health-check) Add health check endpoint
   * e7d0965 (main) Add GitHub Actions CI pipeline and demo runner script
   ```
3. Explain:
   - *"We followed an Issue ➔ Branch ➔ Edit ➔ Test ➔ Commit ➔ PR workflow."*
   - *"The `feature/health-check` branch contains only the isolated changes for the health-check feature, keeping `main` clean."*

---

## 💡 Master Question & Answer Bank

### Q1: What is the difference between FastAPI and traditional frameworks like Flask?
> **Answer:** Flask is a minimalist WSGI framework where routing, serialization, validation, and documentation must be added with third-party extensions. FastAPI is an asynchronous ASGI framework built on Pydantic and Starlette. It automatically performs request validation, response serialization, and Swagger UI generation using standard Python type hints.

### Q2: What is the purpose of Pydantic in this project?
> **Answer:** Pydantic enforces data contracts. It parses incoming JSON payloads and validates data types, string lengths, and custom business rules. If invalid data is sent, Pydantic immediately returns an HTTP 422 error, protecting the application code from processing corrupt data.

### Q3: Why does `POST /tasks` return HTTP 201 instead of HTTP 200?
> **Answer:** Under REST HTTP specifications, `200 OK` indicates a general successful request. However, `201 Created` specifically indicates that a brand-new resource was created on the server and provides the newly assigned resource ID.

### Q4: Why does `DELETE /tasks/{id}` return HTTP 204 No Content?
> **Answer:** HTTP 204 indicates that the server successfully fulfilled the request, and there is no response entity body to return to the client.

### Q5: How do your tests remain isolated in Project 2?
> **Answer:** We created an automated pytest fixture:
> ```python
> @pytest.fixture(autouse=True)
> def run_before_and_after_each_test():
>     reset_db()
>     yield
>     reset_db()
> ```
> `autouse=True` tells pytest to run this fixture for every test function. It clears the dictionary before the test runs and cleans it up after, ensuring test order never causes false failures.

### Q6: What is the difference between `git add` and `git commit`?
> **Answer:** `git add` moves modified files from the Working Directory into the Staging Area (the Index), selecting which files will be included in the next snapshot. `git commit` takes everything in the Staging Area and records an immutable, cryptographically hashed snapshot in the local Git history.

---

## 🔍 Line-by-Line Code Breakdown

### Project 1: `project1_basic/main.py`
- `app = FastAPI(...)`: Instantiates the central application object.
- `@app.get("/")`: Decorator mapping HTTP GET requests on `/` to `read_root()`.
- `return {"message": "..."}`: Python dictionary returned; FastAPI serializes it to JSON and sends status 200.
- `@app.get("/health")`: Decorator for health monitoring endpoint.
- `return {"status": "ok"}`: Standard health status payload.

### Project 2: `project2_crud/main.py`
- `tasks_db = {}`: In-memory Python dictionary storing tasks in RAM.
- `class TaskBase(BaseModel)`: Base schema with `title` and `completed` fields.
- `title: str = Field(..., min_length=1, max_length=100)`: Constrains length.
- `@field_validator("title")`: Validates that titles cannot be blank whitespace.
- `class TaskUpdate(BaseModel)`: Schema with optional fields for partial updates via PUT.
- `class TaskResponse(BaseModel)`: Output schema ensuring integer `id` is returned.
- `status_code=status.HTTP_201_CREATED`: Overrides default 200 for task creation.
- `raise HTTPException(status_code=404, detail=...)`: Halts execution and sends error JSON when task ID is not found.
