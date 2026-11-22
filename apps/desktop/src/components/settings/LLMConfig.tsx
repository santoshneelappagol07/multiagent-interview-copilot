import React from 'react';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
// LLM provider configuration cards

export const LLMConfig: React.FC = () => {
  const configs = [
    {
      mode: 'Fast Mode',
      target: '< 3.0s Latency',
      provider: 'Groq Cloud / Cerebras',
      model: 'Llama-3.1 8B Instant',
      description: 'Used for immediate first-reaction interview answers with mandatory RAG context.',
    },
    {
      mode: 'Reasoning Mode',
      target: 'High Accuracy',
      provider: 'Google Gemini',
      model: 'Gemini 2.0 Flash',
      description: 'Used for system design, detailed algorithms, and nuanced project explanations.',
    },
    {
      mode: 'Research Mode',
      target: 'Deep Analysis',
      provider: 'Groq Cloud',
      model: 'Llama-3.3 70B Versatile',
      description: 'Used for multi-step scenario evaluations and exhaustive technical breakdown.',
    },
  ];

  return (
    <div className="space-y-3">
      {configs.map((c) => (
        <Card key={c.mode} className="p-4 bg-slate-900 border-slate-800">
          <div className="flex items-start justify-between">
            <div>
              <div className="flex items-center gap-2">
                <h4 className="text-sm font-semibold text-slate-100">{c.mode}</h4>
                <Badge variant="success">{c.target}</Badge>
              </div>
              <p className="text-xs text-slate-400 mt-1">{c.description}</p>
            </div>
            <div className="text-right font-mono text-xs text-emerald-400">
              <div>{c.provider}</div>
              <div className="text-[11px] text-slate-500">{c.model}</div>
            </div>
          </div>
        </Card>
      ))}
    </div>
  );
};
