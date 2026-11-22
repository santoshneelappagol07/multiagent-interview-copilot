# AI Voice Copilot - Development Runner (Windows)
$ErrorActionPreference = "Stop"

Write-Host "=== Starting AI Voice Copilot Development Environment ===" -ForegroundColor Cyan

# 1. Start Python FastAPI Backend
Write-Host "Starting Python Backend on http://127.0.0.1:8000..." -ForegroundColor Yellow
$backendJob = Start-Process -FilePath "apps\backend\.venv\Scripts\python.exe" `
    -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload" `
    -WorkingDirectory "apps\backend" `
    -PassThru

# 2. Start Tauri Desktop App
Write-Host "Starting Tauri 2 Desktop Shell..." -ForegroundColor Yellow
Set-Location "apps\desktop"
try {
    pnpm tauri dev
} finally {
    Set-Location "../.."
    Write-Host "`nStopping background processes..." -ForegroundColor Gray
    if ($backendJob -and -not $backendJob.HasExited) {
        Stop-Process -Id $backendJob.Id -Force
    }
    Write-Host "Clean exit." -ForegroundColor Green
}
