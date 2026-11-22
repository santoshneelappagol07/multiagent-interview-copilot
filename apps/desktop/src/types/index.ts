export type AnswerMode = 'fast' | 'reasoning' | 'research';

export interface TranscriptSegment {
  id: string;
  text: string;
  timestamp: number;
  isQuestion: boolean;
  speakerLabel?: string;
  isPartial?: boolean;
}

export interface GeneratedAnswer {
  id: string;
  question: string;
  answer: string;
  mode: AnswerMode;
  provider: string;
  model: string;
  latencyMs: number;
  sources: string[];
  createdAt: string;
}

export interface DocumentItem {
  id: string;
  filename: string;
  format: string;
  fileSize: number;
  uploadedAt: string;
  status: 'processing' | 'indexed' | 'error';
  chunkCount: number;
  errorMessage?: string;
}

export interface LLMProviderInfo {
  name: string;
  isEnabled: boolean;
  models: string[];
  isHealthy: boolean;
  latencyMs?: number;
}

export interface PerformanceMetrics {
  sttLatencyMs: number;
  retrievalLatencyMs: number;
  llmFirstTokenMs: number;
  totalAnswerMs: number;
}

export interface WebSocketEvent<T = any> {
  event: 'transcription_update' | 'answer_stream' | 'question_detected' | 'status_update' | 'error';
  data: T;
  timestamp: number;
}
