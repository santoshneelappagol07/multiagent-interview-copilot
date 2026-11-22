#!/usr/bin/env bash
set -e

echo "=== Starting AI Voice Copilot Dev Environment ==="

# Trap to kill background backend on exit
trap "trap - SIGTERM && kill -- -$$" SIGINT SIGTERM EXIT

# 1. Start Python backend
echo "Starting Python FastAPI Backend..."
cd apps/backend
./.venv/bin/python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload &
BACKEND_PID=$!
cd ../..

# 2. Start Tauri
echo "Starting Tauri Desktop Shell..."
cd apps/desktop
pnpm tauri dev
