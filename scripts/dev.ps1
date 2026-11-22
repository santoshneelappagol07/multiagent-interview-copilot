# AI Voice Copilot - Development Runner (Windows)
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir
Set-Location $projectRoot

Write-Host "=== Starting AI Voice Copilot Development Environment ===" -ForegroundColor Cyan

# 1. Start Python FastAPI Backend
Write-Host "Starting Python Backend on http://127.0.0.1:8000..." -ForegroundColor Yellow
$backendPython = Join-Path $projectRoot "apps\backend\.venv\Scripts\python.exe"

if (-not (Test-Path $backendPython)) {
    Write-Host "Backend virtual environment not found. Using global python..." -ForegroundColor Gray
    $backendPython = "python"
}

$backendJob = Start-Process -FilePath $backendPython `
    -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload" `
    -WorkingDirectory (Join-Path $projectRoot "apps\backend") `
    -PassThru

Start-Sleep -Seconds 2

# 2. Start Frontend / Desktop App
Set-Location (Join-Path $projectRoot "apps\desktop")

$hasCargo = Get-Command "cargo" -ErrorAction SilentlyContinue

try {
    if ($hasCargo) {
        Write-Host "Cargo detected. Starting native Tauri 2 desktop shell..." -ForegroundColor Green
        pnpm tauri dev
    } else {
        Write-Host "Starting UI in browser mode at http://localhost:5173..." -ForegroundColor Green
        Write-Host "(Install Rust from https://rustup.rs/ whenever you want the native Windows .exe window)" -ForegroundColor Gray
        pnpm dev
    }
} finally {
    Set-Location $projectRoot
    Write-Host "`nStopping backend server..." -ForegroundColor Gray
    if ($backendJob -and -not $backendJob.HasExited) {
        Stop-Process -Id $backendJob.Id -Force
    }
    Write-Host "Clean exit completed." -ForegroundColor Green
}
