import React from 'react';
import { AnswerMode } from '../../types';
import { useAppStore } from '../../stores/appStore';
import { Zap, Brain, Microscope } from 'lucide-react';
import clsx from 'clsx';

export const ModeSelector: React.FC = () => {
  const { answerMode, setAnswerMode } = useAppStore();

  const modes: { id: AnswerMode; label: string; desc: string; icon: React.ComponentType<any>; model: string }[] = [
    {
      id: 'fast',
      label: 'Fast Mode',
      desc: '< 3s Target Latency',
      icon: Zap,
      model: 'Groq / Cerebras Llama-3.1 8B',
    },
    {
      id: 'reasoning',
      label: 'Reasoning Mode',
      desc: 'Technical Depth',
      icon: Brain,
      model: 'Google Gemini 2.0 Flash',
    },
    {
      id: 'research',
      label: 'Research Mode',
      desc: 'Deep Synthesis',
      icon: Microscope,
      model: 'Groq Llama-3.3 70B Versatile',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
      {modes.map((m) => {
        const Icon = m.icon;
        const isSelected = answerMode === m.id;
        return (
          <button
            key={m.id}
            type="button"
            onClick={() => setAnswerMode(m.id)}
            className={clsx(
              'flex items-start gap-3 p-3.5 rounded-xl border text-left transition-all',
              isSelected
                ? 'bg-slate-900 border-emerald-500/80 ring-1 ring-emerald-500/50 shadow-sm'
                : 'bg-slate-950/60 border-slate-800 hover:border-slate-700 text-slate-400'
            )}
          >
            <div
              className={clsx(
                'p-2 rounded-lg border',
                isSelected
                  ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                  : 'bg-slate-800/80 border-slate-700/60 text-slate-400'
              )}
            >
              <Icon className="h-4 w-4" />
            </div>
            <div>
              <div
                className={clsx(
                  'text-xs font-semibold tracking-wide',
                  isSelected ? 'text-slate-100' : 'text-slate-300'
                )}
              >
                {m.label}
              </div>
              <div className="text-[11px] text-slate-400 mt-0.5">{m.desc}</div>
              <div className="text-[10px] font-mono text-emerald-400/90 mt-1">
                {m.model}
              </div>
            </div>
          </button>
        );
      })}
    </div>
  );
};
