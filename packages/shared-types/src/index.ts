export type AnswerMode = 'fast' | 'reasoning' | 'research';

export interface TranscriptSegment {
  id: string;
  text: string;
  timestamp: number;
  isQuestion: boolean;
  speakerLabel?: string;
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

export interface UploadedDocument {
  id: string;
  filename: string;
  format: string;
  fileSize: number;
  uploadedAt: string;
  status: 'processing' | 'indexed' | 'error';
  chunkCount: number;
  errorMessage?: string;
}

export interface LLMProviderStatus {
  name: string;
  isEnabled: boolean;
  models: string[];
  isHealthy: boolean;
  latencyMs?: number;
}
