import { AnswerMode, DocumentItem, GeneratedAnswer, LLMProviderInfo } from '../types';

const API_BASE = 'http://127.0.0.1:8000';

export const api = {
  async generateAnswer(question: string, mode: AnswerMode): Promise<GeneratedAnswer> {
    const res = await fetch(`${API_BASE}/api/generate-answer`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, mode }),
    });
    if (!res.ok) throw new Error(`Generate answer failed: ${res.statusText}`);
    return res.json();
  },

  async generateAnswerStream(
    question: string,
    mode: AnswerMode,
    onToken: (token: string) => void,
    onMeta: (meta: { provider: string; model: string; sources: string[] }) => void,
    onDone: (done: { firstTokenMs?: number; totalMs?: number; totalDurationMs?: number }) => void,
  ): Promise<GeneratedAnswer> {
    const res = await fetch(`${API_BASE}/api/generate-answer-stream`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, mode }),
    });

    if (!res.ok) {
      throw new Error(`Streaming request failed: ${res.statusText}`);
    }

    const reader = res.body?.getReader();
    const decoder = new TextDecoder();
    let accumulatedText = '';
    let provider = 'groq';
    let model = 'llama-3.1-8b-instant';
    let sources: string[] = [];
    let totalLatencyMs = 0;

    if (reader) {
      let buffer = '';
      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        buffer += decoder.decode(value, { stream: true });

        const lines = buffer.split('\n\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const event = JSON.parse(line.slice(6));
              if (event.type === 'token') {
                accumulatedText += event.token;
                onToken(event.token);
              } else if (event.type === 'meta') {
                provider = event.provider || provider;
                model = event.model || model;
                sources = event.sources || sources;
                onMeta({ provider, model, sources });
              } else if (event.type === 'done') {
                totalLatencyMs = event.totalDurationMs || event.totalMs || 0;
                onDone(event);
              }
            } catch (e) {
              // Ignore malformed json chunks
            }
          }
        }
      }
    }

    return {
      id: `ans-${Date.now()}`,
      question,
      answer: accumulatedText,
      mode,
      provider,
      model,
      latencyMs: totalLatencyMs || 500,
      sources,
      createdAt: new Date().toISOString(),
    };
  },

  async listDocuments(): Promise<DocumentItem[]> {
    const res = await fetch(`${API_BASE}/api/documents`);
    if (!res.ok) throw new Error('Failed to load documents');
    return res.json();
  },

  async uploadDocument(file: File): Promise<DocumentItem> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/api/documents/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error('Upload failed');
    return res.json();
  },

  async reindexDocuments(): Promise<{ status: string; filesProcessed: number }> {
    const res = await fetch(`${API_BASE}/api/documents/reindex`, {
      method: 'POST',
    });
    if (!res.ok) throw new Error('Reindex failed');
    return res.json();
  },

  async deleteDocument(id: string): Promise<void> {
    const res = await fetch(`${API_BASE}/api/documents/${id}`, {
      method: 'DELETE',
    });
    if (!res.ok) throw new Error('Failed to delete document');
  },

  async getProviders(): Promise<LLMProviderInfo[]> {
    const res = await fetch(`${API_BASE}/api/config/providers`);
    if (!res.ok) throw new Error('Failed to fetch LLM providers');
    return res.json();
  },

  async getConversationHistory(): Promise<{ turns: Array<{ question: string; answer: string; mode: string }>; totalCount: number }> {
    const res = await fetch(`${API_BASE}/api/conversation/history`);
    if (!res.ok) throw new Error('Failed to load conversation history');
    return res.json();
  },

  async resetConversationHistory(): Promise<void> {
    const res = await fetch(`${API_BASE}/api/conversation/history`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to reset conversation history');
  },
};
