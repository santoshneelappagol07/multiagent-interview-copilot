# Architecture Specification: AI Voice Copilot & Real-Time Interview Assistant

## 1. System Overview

```
 [Remote Session / Interviewer Audio]
                   │
                   ▼ (Getscreen.me playback on local machine)
    ┌──────────────────────────────┐
    │  System Audio Loopback (Rust)│ (CPAL WASAPI Loopback / CoreAudio)
    └──────────────┬───────────────┘
                   │
                   ▼
    ┌──────────────────────────────┐
    │ Preprocessing & Normalization│ (rubato sinc resampler -> 16kHz, DC offset removal)
    └──────────────┬───────────────┘
                   │
                   ▼
    ┌──────────────────────────────┐
    │ Energy VAD / Speech Segmenter│ (Silero / Energy-based VAD)
    └──────────────┬───────────────┘
                   │
                   ▼
    ┌──────────────────────────────┐
    │     STT Inference (Rust)     │ (whisper.cpp / whisper-rs local inference)
    └──────────────┬───────────────┘
                   │ (Tonic gRPC stream: audio_service.proto)
                   ▼
    ┌──────────────────────────────┐
    │    Python FastAPI Backend    │
    │  ┌────────────────────────┐  │
    │  │Question Detection Agent│  │
    │  └───────────┬────────────┘  │
    │              │               │
    │  ┌───────────▼────────────┐  │
    │  │ MANDATORY Local RAG    │  │ ◄── [Document Knowledge Base: PDF/DOCX/TXT]
    │  │ Hybrid Search (Chroma) │  │
    │  └───────────┬────────────┘  │
    │              │               │
    │  ┌───────────▼────────────┐  │
    │  │ Intelligent LLM Router │  │ ──► [Groq: Fast / Cerebras: Fast]
    │  │ & Fallback Chain       │  │ ──► [Gemini: Reasoning / Groq 70B: Research]
    │  └───────────┬────────────┘  │ ──► [Ollama Local Fallback]
    │              │               │
    │  ┌───────────▼────────────┐  │
    │  │Answer Generation Agent │  │
    │  └───────────┬────────────┘  │
    └──────────────┼───────────────┘
                   │ (WebSocket real-time streaming)
                   ▼
    ┌──────────────────────────────┐
    │  React 18 + Tauri 2 Desktop  │
    │  - Live Transcription UI     │
    │  - Instant "Generate Answer" │
    │  - Mode Selector (3 modes)   │
    │  - Document Knowledge Base   │
    │  - Latency Performance HUD   │
    └──────────────────────────────┘
```

## 2. Component Isolation & Responsibilities
- **Rust Core**: Owns the unbuffered real-time audio pipeline, WASAPI loopback, VAD segmentation, and Whisper STT inference. Serves events over low-overhead gRPC.
- **Python Backend**: Owns LLM providers, multi-agent coordination, document chunking/conversion, vector embeddings, SQLite session database, and hybrid RAG retrieval.
- **Tauri Shell**: Native window lifecycle, IPC bridge, permissions, OS tray, and process supervision.
- **React Frontend**: Modern dark-theme responsive UI with sub-16ms render loop, virtualized transcript streaming, and instant trigger button.

## 3. Mandatory Document Retrieval Contract
Every answer generation request (even for general/conceptual questions) queries the local vector index first. The prompt template strictly incorporates:
1. Candidate's uploaded resume/projects/notes (if relevant chunks found).
2. Recent conversation transcript context.
3. System prompt enforcing first-person authentic responses without disclosing artificial assistance.
