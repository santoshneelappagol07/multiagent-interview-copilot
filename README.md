# AI Voice Copilot & Real-Time Interview Assistant

Production-grade, low-latency, cross-platform desktop application (Windows & macOS) providing real-time audio capture of interviewers, continuous speech-to-text, multi-agent AI orchestration, mandatory local document RAG retrieval, and intelligent LLM routing across free and open-source models (Gemini, Groq, Cerebras, Ollama).

## Architecture Highlights
- **Rust Audio Core**: System audio loopback capture (WASAPI / Core Audio), VAD, normalizer/resampler, local Whisper STT engine, and gRPC streaming service.
- **Python Backend**: FastAPI, async SQLAlchemy, ChromaDB vector store, hybrid retrieval, sentence-transformers, multi-agent question understanding & answer generation pipeline.
- **Tauri 2 + React 18**: Ultra-responsive native desktop shell, TypeScript, Tailwind CSS, Zustand, and real-time WebSocket communication.
- **Target Latency**: Sub-3-second first meaningful answer in Fast Mode with mandatory document retrieval.

## System Audio Loopback Mode
Captures the interviewer's voice streamed to your local machine (e.g. through Getscreen.me permanent remote desktop sessions or video conferencing apps) directly from system audio without capturing your local microphone.

## Quick Start
1. Clone or navigate to the repository:
   ```bash
   cd ai-voice-copilot
   ```
2. Copy and configure your environment variables:
   ```bash
   cp .env.example .env
   # Add your GEMINI_API_KEY, GROQ_API_KEY, and CEREBRAS_API_KEY
   ```
3. Run automated setup:
   - On Windows PowerShell: `.\scripts\setup.ps1`
   - On macOS/Linux: `./scripts/setup.sh`
4. Start development mode:
   - On Windows: `.\scripts\dev.ps1`
   - On macOS/Linux: `./scripts/dev.sh`
