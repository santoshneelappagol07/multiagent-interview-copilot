# API & Protocol Specification

## 1. gRPC Protocol (`audio_service.proto`)
Serves real-time transcription from the Rust STT Engine to the Python Backend over `127.0.0.1:50051`.

```protobuf
syntax = "proto3";
package audio_service;

service AudioService {
  rpc StreamTranscriptions (google.protobuf.Empty) returns (stream TranscriptionEvent);
  rpc GetStatus (google.protobuf.Empty) returns (EngineStatusResponse);
  rpc StartCapture (StartCaptureRequest) returns (StartCaptureResponse);
  rpc StopCapture (google.protobuf.Empty) returns (StopCaptureResponse);
  rpc ListDevices (google.protobuf.Empty) returns (DeviceListResponse);
}
```

## 2. WebSocket Real-Time Channel (`ws://127.0.0.1:8000/ws`)
Full-duplex real-time communication between the Python Backend and React Frontend.

### Event Format:
```json
{
  "event": "transcription_update" | "answer_stream" | "question_detected" | "status_update" | "error",
  "data": { ... },
  "timestamp": 1711100000000
}
```

## 3. REST Endpoints (FastAPI)
- `POST /api/generate-answer` - Trigger answer generation for selected or detected question.
- `GET /api/documents` - List all uploaded documents with indexing status.
- `POST /api/documents/upload` - Multipart file upload (PDF, DOCX, TXT).
- `DELETE /api/documents/{id}` - Remove document and drop associated vector chunks.
- `GET /api/documents/{id}/preview` - Retrieve normalized extracted plaintext.
- `GET /api/config/providers` - Get status, latency, and health of Groq, Cerebras, Gemini.
- `PUT /api/config/providers` - Update API keys and fallback priorities.
- `GET /api/metrics` - Real-time latency metrics (STT, RAG, TTFT, Total generation).
- `GET /api/status` - Health check across audio engine, database, and vector store.
