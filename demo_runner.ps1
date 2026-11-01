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
    Write-Host " [1] Run All Automated Tests (Project 1 + Project 2)" -ForegroundColor Green
    Write-Host " [2] Run Project 1 Tests (Basic Greeting API)" -ForegroundColor Green
    Write-Host " [3] Run Project 2 Tests (Task Management CRUD API)" -ForegroundColor Green
    Write-Host " [4] Start Project 1 Live Server (Port 8000 + Swagger Docs)" -ForegroundColor Magenta
    Write-Host " [5] Start Project 2 Live Server (Port 8001 + Swagger Docs)" -ForegroundColor Magenta
    Write-Host " [6] Show Git Branching Graph & Commit History" -ForegroundColor Yellow
    Write-Host " [7] Show Git Diff of feature/health-check against main" -ForegroundColor Yellow
    Write-Host " [8] View Deliverables Checklist (CHECKLIST.md)" -ForegroundColor Cyan
    Write-Host " [9] View Instructor Oral Defense & Code Guide (INSTRUCTOR_DEMO_GUIDE.md)" -ForegroundColor Cyan
    Write-Host " [Q] Quit" -ForegroundColor Red
    Write-Host ""
    $choice = Read-Host "Enter your choice"

    switch ($choice.ToUpper()) {
        "1" {
            Write-Host "`n>>> [1/2] Running Project 1 Tests..." -ForegroundColor Cyan
            Set-Location "$PSScriptRoot\project1_basic"
            & $PythonExe -m pytest -v

            Write-Host "`n>>> [2/2] Running Project 2 Tests..." -ForegroundColor Cyan
            Set-Location "$PSScriptRoot\project2_crud"
            & $PythonExe -m pytest -v
            Set-Location $PSScriptRoot

            Write-Host "`nAll test suites completed! Press Enter to return to menu..." -ForegroundColor Gray
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
            Write-Host "`n>>> Starting Project 1 on http://127.0.0.1:8000" -ForegroundColor Cyan
            Write-Host ">>> Interactive Docs: http://127.0.0.1:8000/docs" -ForegroundColor Yellow
            Write-Host ">>> Press Ctrl+C in this terminal when finished to stop the server.`n" -ForegroundColor Gray
            Set-Location "$PSScriptRoot\project1_basic"
            & $UvicornExe main:app --reload --port 8000
            Set-Location $PSScriptRoot
        }
        "5" {
            Write-Host "`n>>> Starting Project 2 on http://127.0.0.1:8001" -ForegroundColor Cyan
            Write-Host ">>> Interactive Docs: http://127.0.0.1:8001/docs" -ForegroundColor Yellow
            Write-Host ">>> Press Ctrl+C in this terminal when finished to stop the server.`n" -ForegroundColor Gray
            Set-Location "$PSScriptRoot\project2_crud"
            & $UvicornExe main:app --reload --port 8001
            Set-Location $PSScriptRoot
        }
        "6" {
            Write-Host "`n>>> Git Branching Tree and History:" -ForegroundColor Cyan
            git log --graph --oneline --all
            Write-Host "`nPress Enter to return to menu..." -ForegroundColor Gray
            Read-Host
        }
        "7" {
            Write-Host "`n>>> Code Differences for PR (feature/health-check vs main):" -ForegroundColor Cyan
            git diff main...feature/health-check
            Write-Host "`nPress Enter to return to menu..." -ForegroundColor Gray
            Read-Host
        }
        "8" {
            Write-Host "`n>>> Displaying Deliverables Checklist (CHECKLIST.md):`n" -ForegroundColor Cyan
            Get-Content "$PSScriptRoot\CHECKLIST.md" | Out-Host -Paging
            Write-Host "`nPress Enter to return to menu..." -ForegroundColor Gray
            Read-Host
        }
        "9" {
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
            Write-Host "Invalid choice, please select 1-9 or Q." -ForegroundColor Red
            Start-Sleep -Seconds 1
        }
    }
} while ($choice.ToUpper() -ne "Q")
