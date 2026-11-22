# Developer Guide

## Prerequisites
- Rust 1.78+ (via `rustup`)
- Python 3.11+
- Node.js 18+ and `pnpm`
- Windows 10/11 or macOS 12+

## Free LLM API Keys Setup
Get your free API keys from:
1. **Google Gemini**: [Google AI Studio](https://aistudio.google.com/)
2. **Groq**: [Groq Console](https://console.groq.com/)
3. **Cerebras**: [Cerebras Cloud Platform](https://cloud.cerebras.ai/)

Insert them into your `.env` file:
```env
GEMINI_API_KEY=AIzaSy...
GROQ_API_KEY=gsk_...
CEREBRAS_API_KEY=csk-...
```

## Testing
- Backend unit tests:
  ```bash
  cd apps/backend
  pytest
  ```
- Rust unit tests:
  ```bash
  cargo test --workspace
  ```
