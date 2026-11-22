# AI Voice Copilot - Automated Windows Setup Script
$ErrorActionPreference = "Stop"

Write-Host "=== AI Voice Copilot Environment Setup ===" -ForegroundColor Cyan

# 1. Check prerequisites
Write-Host "`n[1/6] Checking prerequisites..." -ForegroundColor Yellow
$missing = @()

if (-not (Get-Command rustc -ErrorAction SilentlyContinue)) { $missing += "Rust (rustup / cargo)" }
if (-not (Get-Command python -ErrorAction SilentlyContinue)) { $missing += "Python 3.11+" }
if (-not (Get-Command node -ErrorAction SilentlyContinue)) { $missing += "Node.js (18+)" }
if (-not (Get-Command pnpm -ErrorAction SilentlyContinue)) { 
    Write-Host "pnpm not found, falling back to npm or installing pnpm via npm..." -ForegroundColor Gray
    if (Get-Command npm -ErrorAction SilentlyContinue) {
        npm install -g pnpm
    } else {
        $missing += "pnpm or npm"
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Missing dependencies: $($missing -join ', ')" -ForegroundColor Red
    Write-Host "Please install them before running setup." -ForegroundColor Red
    exit 1
}
Write-Host "Prerequisites verified." -ForegroundColor Green

# 2. Setup storage directories
Write-Host "`n[2/6] Ensuring storage directories exist..." -ForegroundColor Yellow
$dirs = @(
    "storage/documents/originals",
    "storage/documents/extracted",
    "storage/database",
    "storage/vector-store",
    "logs"
)
foreach ($d in $dirs) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
    }
}
Write-Host "Storage directories ready." -ForegroundColor Green

# 3. Environment configuration
Write-Host "`n[3/6] Checking .env configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example. Please update your API keys (Gemini, Groq, Cerebras)." -ForegroundColor Magenta
} else {
    Write-Host ".env already exists." -ForegroundColor Green
}

# 4. Setup Python virtual environment
Write-Host "`n[4/6] Setting up Python virtual environment..." -ForegroundColor Yellow
Set-Location "apps/backend"
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\pip.exe" install -r requirements.txt
Set-Location "../.."
Write-Host "Python environment setup complete." -ForegroundColor Green

# 5. Setup Frontend dependencies
Write-Host "`n[5/6] Installing desktop frontend dependencies..." -ForegroundColor Yellow
Set-Location "apps/desktop"
pnpm install
Set-Location "../.."
Write-Host "Frontend dependencies installed." -ForegroundColor Green

# 6. Verify Rust Crates build
Write-Host "`n[6/6] Verifying Rust workspace..." -ForegroundColor Yellow
cargo check --workspace
Write-Host "Rust workspace verified." -ForegroundColor Green

Write-Host "`nSetup successfully completed! Run .\scripts\dev.ps1 to start development." -ForegroundColor Cyan
