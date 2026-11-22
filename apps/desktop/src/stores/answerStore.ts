import { create } from 'zustand';
import { GeneratedAnswer } from '../types';

interface AnswerState {
  answers: GeneratedAnswer[];
  streamingText: string;
  isGenerating: boolean;
  activeSources: string[];
  startGeneration: () => void;
  appendStream: (chunk: string) => void;
  finishGeneration: (answer: GeneratedAnswer) => void;
  setSources: (sources: string[]) => void;
  clearCurrent: () => void;
}

export const useAnswerStore = create<AnswerState>((set) => ({
  answers: [],
  streamingText: '',
  isGenerating: false,
  activeSources: [],
  startGeneration: () =>
    set({ isGenerating: true, streamingText: '', activeSources: [] }),
  appendStream: (chunk) =>
    set((state) => ({ streamingText: state.streamingText + chunk })),
  finishGeneration: (answer) =>
    set((state) => ({
      answers: [answer, ...state.answers],
      isGenerating: false,
      streamingText: '',
      activeSources: answer.sources,
    })),
  setSources: (activeSources) => set({ activeSources }),
  clearCurrent: () => set({ streamingText: '', isGenerating: false }),
}));
