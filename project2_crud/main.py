from fastapi import FastAPI, HTTPException, status, Path
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

# Initialize the FastAPI application
app = FastAPI(
    title="Task Management API",
    description="A complete CRUD API demonstrating Pydantic validation, status codes, and error handling.",
    version="1.0.0"
)

# ---------------------------------------------------------
# IN-MEMORY DATABASE
# ---------------------------------------------------------
# A Python dictionary stores task records in RAM during runtime.
# IMPORTANT: Data stored here is ephemeral and is wiped when the server restarts.
tasks_db: dict[int, dict] = {}
task_id_counter: int = 0


# ---------------------------------------------------------
# PYDANTIC SCHEMAS (DATA VALIDATION & SERIALIZATION)
# ---------------------------------------------------------

class TaskBase(BaseModel):
    """Base schema shared between create and response models."""
    title: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Task title (cannot be empty, max 100 characters)"
    )
    completed: bool = Field(
        default=False,
        description="Whether the task has been finished"
    )

    @field_validator("title")
    @classmethod
    def validate_title_not_whitespace(cls, value: str) -> str:
        """Reject titles that are only whitespace characters."""
        trimmed = value.strip()
        if not trimmed:
            raise ValueError("Task title cannot be empty or blank whitespace.")
        return trimmed


class TaskCreate(TaskBase):
    """Schema expected in the request body when creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task. Fields are optional."""
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=100,
        description="Updated task title"
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Updated task completion status"
    )

    @field_validator("title")
    @classmethod
    def validate_title_not_whitespace(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            trimmed = value.strip()
            if not trimmed:
                raise ValueError("Task title cannot be empty or blank whitespace.")
            return trimmed
        return value


class TaskResponse(BaseModel):
    """Schema returned to the client, including the server-generated task ID."""
    id: int = Field(..., description="Unique integer ID of the task")
    title: str = Field(..., description="Title of the task")
    completed: bool = Field(..., description="Completion status of the task")


def reset_db() -> None:
    """Helper function to clear database state (useful for automated testing)."""
    global tasks_db, task_id_counter
    tasks_db.clear()
    task_id_counter = 0


# ---------------------------------------------------------
# API ROUTES (ENDPOINTS)
# ---------------------------------------------------------

@app.get("/", tags=["General"])
def read_root():
    """Welcome route providing guidance to API consumers."""
    return {
        "message": "Welcome to the Task Management API!",
        "documentation": "/docs",
        "dashboard": "/dashboard"
    }


@app.get("/dashboard", response_class=HTMLResponse, tags=["General"])
def serve_dashboard():
    """Serves an interactive single-page web dashboard for live demonstrations."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Task Management Studio</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Inter', sans-serif; }
    body { background: #0f172a; color: #f8fafc; min-height: 100vh; display: flex; flex-direction: column; align-items: center; padding: 40px 20px; }
    .container { width: 100%; max-width: 680px; }
    .header { text-align: center; margin-bottom: 30px; }
    .badge { display: inline-block; background: rgba(56, 189, 248, 0.15); color: #38bdf8; padding: 4px 12px; border-radius: 9999px; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 12px; border: 1px solid rgba(56, 189, 248, 0.3); }
    h1 { font-size: 28px; font-weight: 700; margin-bottom: 8px; background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    p.subtitle { color: #94a3b8; font-size: 14px; }
    .nav-links { display: flex; justify-content: center; gap: 16px; margin-top: 14px; }
    .nav-links a { color: #38bdf8; text-decoration: none; font-size: 13px; font-weight: 500; padding: 4px 10px; border-radius: 6px; background: rgba(255,255,255,0.05); transition: background 0.2s; }
    .nav-links a:hover { background: rgba(255,255,255,0.1); }
    .card { background: #1e293b; border: 1px solid #334155; border-radius: 14px; padding: 24px; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3); margin-bottom: 24px; }
    .input-group { display: flex; gap: 12px; }
    input[type="text"] { flex: 1; background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 12px 16px; color: #f8fafc; font-size: 14px; outline: none; transition: border-color 0.2s; }
    input[type="text"]:focus { border-color: #38bdf8; }
    button.btn-primary { background: linear-gradient(135deg, #0284c7, #2563eb); color: white; border: none; border-radius: 8px; padding: 12px 20px; font-size: 14px; font-weight: 600; cursor: pointer; transition: transform 0.1s, opacity 0.2s; }
    button.btn-primary:hover { opacity: 0.95; }
    button.btn-primary:active { transform: scale(0.98); }
    .stats { display: flex; justify-content: space-between; padding: 12px 16px; background: rgba(15, 23, 42, 0.6); border-radius: 8px; margin-bottom: 16px; font-size: 13px; color: #94a3b8; }
    .stats span strong { color: #f8fafc; }
    .task-list { display: flex; flex-direction: column; gap: 10px; }
    .task-item { display: flex; align-items: center; justify-content: space-between; background: #0f172a; border: 1px solid #334155; border-radius: 10px; padding: 14px 16px; transition: border-color 0.2s, background 0.2s; }
    .task-item:hover { border-color: #475569; }
    .task-left { display: flex; align-items: center; gap: 12px; flex: 1; }
    .checkbox { width: 20px; height: 20px; border-radius: 6px; border: 2px solid #64748b; display: flex; align-items: center; justify-content: center; cursor: pointer; transition: all 0.2s; }
    .checkbox.checked { background: #10b981; border-color: #10b981; }
    .task-title { font-size: 14px; color: #f1f5f9; transition: color 0.2s, text-decoration 0.2s; word-break: break-word; }
    .task-title.completed { text-decoration: line-through; color: #64748b; }
    .task-id { font-size: 11px; font-weight: 600; color: #64748b; padding: 2px 6px; background: rgba(255,255,255,0.05); border-radius: 4px; }
    .btn-delete { background: none; border: none; color: #ef4444; cursor: pointer; padding: 6px 10px; font-size: 13px; border-radius: 6px; transition: background 0.2s; }
    .btn-delete:hover { background: rgba(239, 68, 68, 0.15); }
    .empty-state { text-align: center; padding: 32px 16px; color: #64748b; font-size: 14px; }
    .toast { position: fixed; bottom: 24px; right: 24px; padding: 12px 20px; border-radius: 8px; font-size: 13px; font-weight: 500; display: none; z-index: 100; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.4); }
    .toast.error { background: #ef4444; color: white; }
    .toast.success { background: #10b981; color: white; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="badge">FastAPI + Pydantic v2</div>
      <h1>Task Management Studio</h1>
      <p class="subtitle">Live CRUD Operations & In-Memory Persistence Demo</p>
      <div class="nav-links">
        <a href="/docs" target="_blank">📖 Swagger UI Docs</a>
        <a href="/redoc" target="_blank">📋 ReDoc</a>
        <a href="/tasks" target="_blank">🔌 Raw JSON API</a>
      </div>
    </div>

    <div class="card">
      <form id="taskForm" class="input-group">
        <input type="text" id="taskTitle" placeholder="Enter task title (try whitespace to test validation)..." autofocus autocomplete="off" />
        <button type="submit" class="btn-primary">Add Task</button>
      </form>
    </div>

    <div class="card">
      <div class="stats">
        <span>Total: <strong id="totalCount">0</strong></span>
        <span>Pending: <strong id="pendingCount">0</strong></span>
        <span>Completed: <strong id="completedCount">0</strong></span>
      </div>
      <div id="taskList" class="task-list">
        <div class="empty-state">No tasks yet. Create your first task above!</div>
      </div>
    </div>
  </div>

  <div id="toast" class="toast"></div>

  <script>
    const taskForm = document.getElementById('taskForm');
    const taskTitleInput = document.getElementById('taskTitle');
    const taskList = document.getElementById('taskList');
    const toast = document.getElementById('toast');

    function showToast(message, type = 'error') {
      toast.textContent = message;
      toast.className = 'toast ' + type;
      toast.style.display = 'block';
      setTimeout(() => { toast.style.display = 'none'; }, 3500);
    }

    async function fetchTasks() {
      try {
        const res = await fetch('/tasks');
        const tasks = await res.json();
        renderTasks(tasks);
      } catch (err) {
        showToast('Failed to load tasks from server.');
      }
    }

    function renderTasks(tasks) {
      document.getElementById('totalCount').textContent = tasks.length;
      document.getElementById('completedCount').textContent = tasks.filter(t => t.completed).length;
      document.getElementById('pendingCount').textContent = tasks.filter(t => !t.completed).length;

      if (tasks.length === 0) {
        taskList.innerHTML = '<div class="empty-state">No tasks in memory. Add one above!</div>';
        return;
      }

      taskList.innerHTML = tasks.map(t => `
        <div class="task-item">
          <div class="task-left">
            <div class="checkbox ${t.completed ? 'checked' : ''}" onclick="toggleTask(${t.id}, ${!t.completed})">
              ${t.completed ? '✓' : ''}
            </div>
            <span class="task-id">#${t.id}</span>
            <span class="task-title ${t.completed ? 'completed' : ''}">${escapeHtml(t.title)}</span>
          </div>
          <button class="btn-delete" onclick="deleteTask(${t.id})">Delete</button>
        </div>
      `).join('');
    }

    function escapeHtml(text) {
      const div = document.createElement('div');
      div.innerText = text;
      return div.innerHTML;
    }

    taskForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = taskTitleInput.value;
      try {
        const res = await fetch('/tasks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ title, completed: false })
        });
        if (!res.ok) {
          const err = await res.json();
          const detail = err.detail?.[0]?.msg || JSON.stringify(err.detail);
          showToast('Validation Error (HTTP ' + res.status + '): ' + detail);
          return;
        }
        taskTitleInput.value = '';
        showToast('Task created successfully! (HTTP 201)', 'success');
        fetchTasks();
      } catch (err) {
        showToast('Error communicating with server.');
      }
    });

    async function toggleTask(id, completed) {
      try {
        const res = await fetch('/tasks/' + id, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ completed })
        });
        if (!res.ok) throw new Error();
        fetchTasks();
      } catch (err) {
        showToast('Failed to update task.');
      }
    }

    async function deleteTask(id) {
      try {
        const res = await fetch('/tasks/' + id, { method: 'DELETE' });
        if (res.status === 204) {
          showToast('Task #' + id + ' deleted (HTTP 204)', 'success');
          fetchTasks();
        } else {
          showToast('Failed to delete task.');
        }
      } catch (err) {
        showToast('Error deleting task.');
      }
    }

    fetchTasks();
  </script>
</body>
</html>"""


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a new task"
)
def create_task(task_in: TaskCreate):
    """
    Create a new task in memory:
    - **title**: Non-empty text string
    - **completed**: Boolean flag (defaults to false)
    Returns HTTP 201 Created with the persisted task record.
    """
    global task_id_counter
    task_id_counter += 1
    new_task = {
        "id": task_id_counter,
        "title": task_in.title,
        "completed": task_in.completed,
    }
    tasks_db[task_id_counter] = new_task
    return new_task


@app.get(
    "/tasks",
    response_model=List[TaskResponse],
    status_code=status.HTTP_200_OK,
    tags=["Tasks"],
    summary="List all tasks"
)
def list_tasks():
    """Retrieve all current tasks stored in memory."""
    return list(tasks_db.values())


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    tags=["Tasks"],
    summary="Get a specific task by ID"
)
def get_task(task_id: int = Path(..., ge=1, description="Unique positive ID of the task")):
    """
    Retrieve details of a single task by its integer identifier.
    Returns HTTP 404 if the task ID does not exist.
    """
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )
    return task


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    status_code=status.HTTP_200_OK,
    tags=["Tasks"],
    summary="Update an existing task"
)
def update_task(
    task_id: int = Path(..., ge=1, description="Unique positive ID of the task to update"),
    task_update: TaskUpdate = ...
):
    """
    Update fields of an existing task:
    - **title**: New title (optional)
    - **completed**: New boolean status (optional)
    Returns HTTP 404 if the task does not exist.
    """
    task = tasks_db.get(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )

    if task_update.title is not None:
        task["title"] = task_update.title
    if task_update.completed is not None:
        task["completed"] = task_update.completed

    tasks_db[task_id] = task
    return task


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete a task"
)
def delete_task(task_id: int = Path(..., ge=1, description="Unique positive ID of the task to delete")):
    """
    Delete a task from the in-memory database.
    Returns HTTP 204 No Content upon success, or HTTP 404 if the task was not found.
    """
    if task_id not in tasks_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with ID {task_id} not found."
        )
    del tasks_db[task_id]
    return None
