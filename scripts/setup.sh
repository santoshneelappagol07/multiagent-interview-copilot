#!/usr/bin/env bash
set -e

echo "=== AI Voice Copilot Environment Setup (macOS / Linux) ==="

# 1. Prerequisites check
echo "\n[1/6] Checking prerequisites..."
command -v rustc >/dev/null 2>&1 || { echo "Rust (cargo) is required."; exit 1; }
command -v python3 >/dev/null 2>&1 || { echo "Python 3.11+ is required."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "Node.js is required."; exit 1; }
command -v pnpm >/dev/null 2>&1 || { echo "Installing pnpm..."; npm install -g pnpm; }

# 2. Storage directories
echo "\n[2/6] Ensuring storage directories exist..."
mkdir -p storage/documents/originals storage/documents/extracted storage/database storage/vector-store logs

# 3. Environment file
echo "\n[3/6] Checking .env file..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Created .env from .env.example. Please populate your API keys."
fi

# 4. Python venv
echo "\n[4/6] Setting up Python virtual environment..."
cd apps/backend
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
./.venv/bin/pip install --upgrade pip
./.venv/bin/pip install -r requirements.txt
cd ../..

# 5. Frontend
echo "\n[5/6] Installing desktop dependencies..."
cd apps/desktop
pnpm install
cd ../..

# 6. Rust check
echo "\n[6/6] Checking Rust workspace..."
cargo check --workspace

echo "\nSetup completed successfully! Run ./scripts/dev.sh to launch."
