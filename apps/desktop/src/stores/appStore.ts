import { create } from 'zustand';
import { AnswerMode, PerformanceMetrics } from '../types';

interface AppState {
  isCapturing: boolean;
  wsConnected: boolean;
  answerMode: AnswerMode;
  metrics: PerformanceMetrics;
  setCapturing: (capturing: boolean) => void;
  setWsConnected: (connected: boolean) => void;
  setAnswerMode: (mode: AnswerMode) => void;
  updateMetrics: (metrics: Partial<PerformanceMetrics>) => void;
}

export const useAppStore = create<AppState>((set) => ({
  isCapturing: false,
  wsConnected: false,
  answerMode: 'fast',
  metrics: {
    sttLatencyMs: 0,
    retrievalLatencyMs: 0,
    llmFirstTokenMs: 0,
    totalAnswerMs: 0,
  },
  setCapturing: (capturing) => set({ isCapturing: capturing }),
  setWsConnected: (connected) => set({ wsConnected: connected }),
  setAnswerMode: (answerMode) => set({ answerMode }),
  updateMetrics: (newMetrics) =>
    set((state) => ({ metrics: { ...state.metrics, ...newMetrics } })),
}));
