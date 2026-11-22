import React, { useRef, useEffect } from 'react';
import { useTranscriptStore } from '../../stores/transcriptStore';
import { QuestionCard } from './QuestionCard';
import { Volume2 } from 'lucide-react';
import clsx from 'clsx';

export const TranscriptView: React.FC = () => {
  const segments = useTranscriptStore((state) => state.segments);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [segments]);

  return (
    <div className="space-y-3">
      {segments.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-20 text-slate-500 border border-dashed border-slate-800 rounded-xl bg-slate-900/30">
          <Volume2 className="h-8 w-8 mb-2 opacity-50 text-slate-400" />
          <p className="text-sm">No audio detected yet.</p>
          <p className="text-xs text-slate-600 mt-1">
            System audio from interviewer will transcribe here in real time.
          </p>
        </div>
      ) : (
        segments.map((seg) => {
          if (seg.isQuestion) {
            return (
              <QuestionCard
                key={seg.id}
                question={seg.text}
                timestamp={seg.timestamp}
              />
            );
          }

          return (
            <div
              key={seg.id}
              className={clsx(
                'p-3.5 rounded-xl border transition-all text-sm',
                seg.isPartial
                  ? 'bg-slate-900/40 border-slate-800/50 text-slate-400 italic animate-pulse'
                  : 'bg-slate-900 border-slate-800 text-slate-200'
              )}
            >
              <div className="flex items-center justify-between text-[11px] text-slate-500 mb-1 font-mono">
                <span>Interviewer (System Audio)</span>
                <span>{new Date(seg.timestamp).toLocaleTimeString()}</span>
              </div>
              <p className="leading-relaxed">{seg.text}</p>
            </div>
          );
        })
      )}
      <div ref={bottomRef} />
    </div>
  );
};
