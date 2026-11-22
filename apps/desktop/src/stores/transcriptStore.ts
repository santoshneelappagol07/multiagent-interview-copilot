import { create } from 'zustand';
import { TranscriptSegment } from '../types';

interface TranscriptState {
  segments: TranscriptSegment[];
  selectedQuestion: string | null;
  addSegment: (segment: TranscriptSegment) => void;
  updatePartialSegment: (text: string) => void;
  setSelectedQuestion: (question: string | null) => void;
  clearTranscript: () => void;
}

export const useTranscriptStore = create<TranscriptState>((set) => ({
  segments: [],
  selectedQuestion: null,
  addSegment: (segment) =>
    set((state) => ({
      segments: [...state.segments.filter((s) => !s.isPartial), segment],
    })),
  updatePartialSegment: (text) =>
    set((state) => {
      const filtered = state.segments.filter((s) => !s.isPartial);
      if (!text.trim()) return { segments: filtered };
      const partial: TranscriptSegment = {
        id: 'partial-latest',
        text,
        timestamp: Date.now(),
        isQuestion: text.includes('?'),
        isPartial: true,
      };
      return { segments: [...filtered, partial] };
    }),
  setSelectedQuestion: (selectedQuestion) => set({ selectedQuestion }),
  clearTranscript: () => set({ segments: [], selectedQuestion: null }),
}));
