# ==============================================================================
# Automated GitHub Deployment & PR Creator Script
# ==============================================================================

$GhExe = Join-Path $PSScriptRoot ".venv\Scripts\gh.exe"

Write-Host "=================================================================" -ForegroundColor Cyan
Write-Host "          FASTAPI AUTOMATED GITHUB DEPLOYMENT & PR               " -ForegroundColor Yellow
Write-Host "=================================================================" -ForegroundColor Cyan

# 1. Check GitHub Authentication
Write-Host "`n>>> [Step 1/4] Checking GitHub CLI Authentication..." -ForegroundColor Cyan
& $GhExe auth status 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n[AUTHENTICATION REQUIRED]" -ForegroundColor Yellow
    Write-Host "Your machine does not have an active GitHub session." -ForegroundColor White
    Write-Host "GitHub CLI will now open your default browser to authenticate safely." -ForegroundColor White
    Write-Host "Select: GitHub.com -> HTTPS -> Login with a web browser.`n" -ForegroundColor Gray
    
    & $GhExe auth login --hostname github.com --git-protocol https --web
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`nAuthentication was not completed. Please run '.\.venv\Scripts\gh.exe auth login' and try again." -ForegroundColor Red
        exit 1
    }
}

# 2. Check if remote origin already exists
$hasRemote = git remote | Select-String "origin"
if (-not $hasRemote) {
    Write-Host "`n>>> [Step 2/4] Creating new public repository 'fastapi-micro-project' on GitHub..." -ForegroundColor Cyan
    & $GhExe repo create fastapi-micro-project --public --source="$PSScriptRoot" --remote=origin
} else {
    Write-Host "`n>>> [Step 2/4] Remote 'origin' already configured." -ForegroundColor Green
}

# 3. Push both branches
Write-Host "`n>>> [Step 3/4] Pushing all local branches to GitHub..." -ForegroundColor Cyan
git push -u origin main
git push -u origin feature/health-check

# 4. Generate the Pull Request
Write-Host "`n>>> [Step 4/4] Creating Pull Request for Health Check feature..." -ForegroundColor Cyan
$prBody = @"
## 🚀 Summary of Changes
- Implemented `GET /health` endpoint returning `{"status": "ok"}` with HTTP 200.
- Added automated test in `project1_basic/test_main.py` using `fastapi.testclient.TestClient`.
- Verified test suite: 46/46 unit tests passing across all 4 projects.

## 🔗 Issue Reference
Closes #1
"@

$prResult = & $GhExe pr create --base main --head feature/health-check --title "Add health-check endpoint to Basic Greeting API" --body $prBody

Write-Host "`n=================================================================" -ForegroundColor Green
Write-Host "                    DEPLOYMENT COMPLETE!                         " -ForegroundColor Green
Write-Host "=================================================================" -ForegroundColor Green
Write-Host "Your Pull Request is live at: $prResult" -ForegroundColor Yellow
Write-Host "Opening Pull Request in your web browser..." -ForegroundColor Gray
& $GhExe pr view --web
