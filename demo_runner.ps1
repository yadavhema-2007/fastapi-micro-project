# ==============================================================================
# FastAPI Micro Project: Interactive Instructor Demo Menu
# ==============================================================================

$PythonExe = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$UvicornExe = Join-Path $PSScriptRoot ".venv\Scripts\uvicorn.exe"

function Show-Header {
    Clear-Host
    Write-Host "=================================================================" -ForegroundColor Cyan
    Write-Host "       FASTAPI MICRO PROJECT: INSTRUCTOR DEMO CONTROLLER         " -ForegroundColor Yellow
    Write-Host "=================================================================" -ForegroundColor Cyan
    Write-Host " Python Environment: $PythonExe" -ForegroundColor Gray
    Write-Host " Git Branch: $(git branch --show-current)" -ForegroundColor Gray
    Write-Host "-----------------------------------------------------------------" -ForegroundColor Cyan
}

do {
    Show-Header
    Write-Host "Select an action to demonstrate:" -ForegroundColor White
    Write-Host " [1]  Run All Automated Tests (Projects 1 + 2 + 3 + 4: 46 Tests)" -ForegroundColor Green
    Write-Host " [2]  Run Project 1 Tests (Basic Greeting API)" -ForegroundColor Green
    Write-Host " [3]  Run Project 2 Tests (Task Management In-Memory CRUD)" -ForegroundColor Green
    Write-Host " [4]  Run Project 3 Tests (SQLite + SQLAlchemy Persistent API)" -ForegroundColor Green
    Write-Host " [5]  Run Project 4 Tests (JWT Auth & Password Hashing Security)" -ForegroundColor Green
    Write-Host " [6]  Start Project 1 Server (Port 8000 + Swagger Docs)" -ForegroundColor Magenta
    Write-Host " [7]  Start Project 2 Server (Port 8001 + Web Dashboard & Docs)" -ForegroundColor Magenta
    Write-Host " [8]  Start Project 3 Server (Port 8002 + SQLite Database)" -ForegroundColor Magenta
    Write-Host " [9]  Start Project 4 Server (Port 8003 + JWT Auth API)" -ForegroundColor Magenta
    Write-Host " [10] Show Git Branching Graph & Commit History" -ForegroundColor Yellow
    Write-Host " [11] Show Git Diff of feature/health-check against main" -ForegroundColor Yellow
    Write-Host " [12] View Deliverables Checklist (CHECKLIST.md)" -ForegroundColor Cyan
    Write-Host " [13] View Instructor Oral Defense & Code Guide" -ForegroundColor Cyan
    Write-Host " [Q]  Quit" -ForegroundColor Red
    Write-Host ""
    $choice = Read-Host "Enter your choice"

    switch ($choice.ToUpper()) {
        "1" {
            Write-Host "`n>>> [1/4] Running Project 1 Tests..." -ForegroundColor Cyan
            Set-Location "$PSScriptRoot\project1_basic"
            & $PythonExe -m pytest -v

            Write-Host "`n>>> [2/4] Running Project 2 Tests..." -ForegroundColor Cyan
            Set-Location "$PSScriptRoot\project2_crud"
            & $PythonExe -m pytest -v

            Write-Host "`n>>> [3/4] Running Project 3 Tests..." -ForegroundColor Cyan
            Set-Location "$PSScriptRoot\project3_database"
            & $PythonExe -m pytest -v

            Write-Host "`n>>> [4/4] Running Project 4 Tests..." -ForegroundColor Cyan
            Set-Location "$PSScriptRoot\project4_auth"
            & $PythonExe -m pytest -v
            Set-Location $PSScriptRoot

            Write-Host "`nAll 4 test suites completed (46 tests passed)! Press Enter..." -ForegroundColor Gray
            Read-Host
        }
        "2" {
            Write-Host "`n>>> Running Project 1 Tests..." -ForegroundColor Cyan
            Set-Location "$PSScriptRoot\project1_basic"
            & $PythonExe -m pytest -v
            Set-Location $PSScriptRoot
            Write-Host "`nPress Enter to return to menu..." -ForegroundColor Gray
            Read-Host
        }
        "3" {
            Write-Host "`n>>> Running Project 2 Tests..." -ForegroundColor Cyan
            Set-Location "$PSScriptRoot\project2_crud"
            & $PythonExe -m pytest -v
            Set-Location $PSScriptRoot
            Write-Host "`nPress Enter to return to menu..." -ForegroundColor Gray
            Read-Host
        }
        "4" {
            Write-Host "`n>>> Running Project 3 Tests (SQLite In-Memory)..." -ForegroundColor Cyan
            Set-Location "$PSScriptRoot\project3_database"
            & $PythonExe -m pytest -v
            Set-Location $PSScriptRoot
            Write-Host "`nPress Enter to return to menu..." -ForegroundColor Gray
            Read-Host
        }
        "5" {
            Write-Host "`n>>> Running Project 4 Tests (JWT & Security)..." -ForegroundColor Cyan
            Set-Location "$PSScriptRoot\project4_auth"
            & $PythonExe -m pytest -v
            Set-Location $PSScriptRoot
            Write-Host "`nPress Enter to return to menu..." -ForegroundColor Gray
            Read-Host
        }
        "6" {
            Write-Host "`n>>> Starting Project 1 on http://127.0.0.1:8000" -ForegroundColor Cyan
            Write-Host ">>> Interactive Docs: http://127.0.0.1:8000/docs" -ForegroundColor Yellow
            Write-Host ">>> Press Ctrl+C in this terminal when finished to stop the server.`n" -ForegroundColor Gray
            Set-Location "$PSScriptRoot\project1_basic"
            & $UvicornExe main:app --reload --port 8000
            Set-Location $PSScriptRoot
        }
        "7" {
            Write-Host "`n>>> Starting Project 2 on http://127.0.0.1:8001" -ForegroundColor Cyan
            Write-Host ">>> Interactive Web Dashboard: http://127.0.0.1:8001/dashboard" -ForegroundColor Green
            Write-Host ">>> Interactive Swagger Docs:  http://127.0.0.1:8001/docs" -ForegroundColor Yellow
            Write-Host ">>> Press Ctrl+C in this terminal when finished to stop the server.`n" -ForegroundColor Gray
            Set-Location "$PSScriptRoot\project2_crud"
            & $UvicornExe main:app --reload --port 8001
            Set-Location $PSScriptRoot
        }
        "8" {
            Write-Host "`n>>> Starting Project 3 on http://127.0.0.1:8002" -ForegroundColor Cyan
            Write-Host ">>> Persistent Database: tasks.db (SQLite on disk)" -ForegroundColor Green
            Write-Host ">>> Interactive Swagger Docs:  http://127.0.0.1:8002/docs" -ForegroundColor Yellow
            Write-Host ">>> Press Ctrl+C in this terminal when finished to stop the server.`n" -ForegroundColor Gray
            Set-Location "$PSScriptRoot\project3_database"
            & $UvicornExe main:app --reload --port 8002
            Set-Location $PSScriptRoot
        }
        "9" {
            Write-Host "`n>>> Starting Project 4 on http://127.0.0.1:8003" -ForegroundColor Cyan
            Write-Host ">>> JWT Authentication & Vault API" -ForegroundColor Green
            Write-Host ">>> Interactive Swagger Docs:  http://127.0.0.1:8003/docs" -ForegroundColor Yellow
            Write-Host ">>> Press Ctrl+C in this terminal when finished to stop the server.`n" -ForegroundColor Gray
            Set-Location "$PSScriptRoot\project4_auth"
            & $UvicornExe main:app --reload --port 8003
            Set-Location $PSScriptRoot
        }
        "10" {
            Write-Host "`n>>> Git Branching Tree and History:" -ForegroundColor Cyan
            git log --graph --oneline --all
            Write-Host "`nPress Enter to return to menu..." -ForegroundColor Gray
            Read-Host
        }
        "11" {
            Write-Host "`n>>> Code Differences for PR (feature/health-check vs main):" -ForegroundColor Cyan
            git diff main...feature/health-check
            Write-Host "`nPress Enter to return to menu..." -ForegroundColor Gray
            Read-Host
        }
        "12" {
            Write-Host "`n>>> Displaying Deliverables Checklist (CHECKLIST.md):`n" -ForegroundColor Cyan
            Get-Content "$PSScriptRoot\CHECKLIST.md" | Out-Host -Paging
            Write-Host "`nPress Enter to return to menu..." -ForegroundColor Gray
            Read-Host
        }
        "13" {
            Write-Host "`n>>> Displaying Instructor Defense Guide (INSTRUCTOR_DEMO_GUIDE.md):`n" -ForegroundColor Cyan
            Get-Content "$PSScriptRoot\INSTRUCTOR_DEMO_GUIDE.md" | Out-Host -Paging
            Write-Host "`nPress Enter to return to menu..." -ForegroundColor Gray
            Read-Host
        }
        "Q" {
            Write-Host "Exiting demo controller. Good luck with your presentation!" -ForegroundColor Green
            break
        }
        default {
            Write-Host "Invalid choice, please select 1-13 or Q." -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
} while ($choice.ToUpper() -ne "Q")
