import React, { useState, useEffect } from 'react';
import { ModeSelector } from '../components/ai/ModeSelector';
import { GenerateButton } from '../components/ai/GenerateButton';
import { AnswerPanel } from '../components/ai/AnswerPanel';
import { Card } from '../components/ui/Card';
import { Input } from '../components/ui/Input';
import { useTranscriptStore } from '../stores/transcriptStore';
import { useAppStore } from '../stores/appStore';
import { useAnswerStore } from '../stores/answerStore';
import { api } from '../services/api';
import toast from 'react-hot-toast';

export const AIPanel: React.FC = () => {
  const { selectedQuestion, setSelectedQuestion } = useTranscriptStore();
  const answerMode = useAppStore((state) => state.answerMode);
  const { startGeneration, appendStream, finishGeneration, setSources, clearCurrent, isGenerating } = useAnswerStore();
  const [customQuestion, setCustomQuestion] = useState('');

  const currentQuestion = selectedQuestion || customQuestion;

  const handleGenerate = async () => {
    if (!currentQuestion.trim() || isGenerating) {
      if (!currentQuestion.trim()) toast.error('Please enter or select a question first.');
      return;
    }

    try {
      startGeneration();
      const startTime = performance.now();

      // Use real-time token streaming for immediate display
      const result = await api.generateAnswerStream(
        currentQuestion,
        answerMode,
        (token) => appendStream(token),
        (meta) => setSources(meta.sources),
        (_done) => {
          // Finished streaming
        }
      );

      const elapsed = Math.round(performance.now() - startTime);
      result.latencyMs = result.latencyMs || elapsed;
      finishGeneration(result);
      toast.success(`Answer generated in ${(result.latencyMs / 1000).toFixed(2)}s`);
    } catch (err: any) {
      clearCurrent();
      toast.error(err.message || 'Generation failed');
    }
  };

  // Keyboard shortcut: Ctrl+Enter or Cmd+Enter to generate
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        handleGenerate();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [currentQuestion, answerMode, isGenerating]);

  return (
    <div className="space-y-5 max-w-5xl mx-auto">
      {/* Mode Selector */}
      <ModeSelector />

      {/* Question Selection Card */}
      <Card className="p-4 bg-slate-900 border-slate-800 space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-xs font-semibold text-slate-300 uppercase tracking-wide flex items-center gap-2">
            Target Interview Question
            <span className="text-[10px] text-slate-500 font-normal">
              (Press <kbd className="px-1.5 py-0.5 rounded bg-slate-800 border border-slate-700 font-mono text-slate-300">Ctrl+Enter</kbd> to generate)
            </span>
          </label>
          {selectedQuestion && (
            <button
              type="button"
              onClick={() => setSelectedQuestion(null)}
              className="text-xs text-slate-500 hover:text-slate-300 transition-colors"
            >
              Clear selection
            </button>
          )}
        </div>

        <Input
          placeholder="e.g. Can you explain your experience designing scalable microservices in Python?"
          value={selectedQuestion || customQuestion}
          onChange={(e) => {
            if (selectedQuestion) setSelectedQuestion(null);
            setCustomQuestion(e.target.value);
          }}
          onKeyDown={(e) => {
            if (e.key === 'Enter' && !e.shiftKey && (e.ctrlKey || e.metaKey)) {
              e.preventDefault();
              handleGenerate();
            }
          }}
        />

        <GenerateButton onGenerate={handleGenerate} disabled={!currentQuestion.trim() || isGenerating} />
      </Card>

      {/* Answer Stream & Response */}
      <AnswerPanel />
    </div>
  );
};
