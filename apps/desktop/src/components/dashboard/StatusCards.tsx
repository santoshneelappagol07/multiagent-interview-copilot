import React from 'react';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Cpu, Radio, Sparkles, Database } from 'lucide-react';
import { useAppStore } from '../../stores/appStore';
import { useDocumentStore } from '../../stores/documentStore';

export const StatusCards: React.FC = () => {
  const isCapturing = useAppStore((state) => state.isCapturing);
  const wsConnected = useAppStore((state) => state.wsConnected);
  const documents = useDocumentStore((state) => state.documents);

  const cards = [
    {
      title: 'Audio Loopback Capture',
      subtitle: 'Capturing Interviewer Audio',
      icon: Radio,
      status: isCapturing ? 'Active' : 'Standby',
      variant: (isCapturing ? 'success' : 'neutral') as 'success' | 'neutral',
      detail: 'CPAL System Audio Loopback',
    },
    {
      title: 'Whisper STT Engine',
      subtitle: 'Local Real-Time Transcription',
      icon: Cpu,
      status: isCapturing ? 'Listening' : 'Ready',
      variant: (isCapturing ? 'success' : 'neutral') as 'success' | 'neutral',
      detail: 'VAD + 16kHz Sinc Resampling',
    },
    {
      title: 'FastAPI Intelligence Backend',
      subtitle: 'gRPC & WebSocket Pipeline',
      icon: Sparkles,
      status: wsConnected ? 'Connected' : 'Offline',
      variant: (wsConnected ? 'success' : 'danger') as 'success' | 'danger',
      detail: 'Multi-Agent Orchestrator',
    },
    {
      title: 'Mandatory Local RAG',
      subtitle: 'Vector Knowledge Base',
      icon: Database,
      status: `${documents.length} Docs Indexed`,
      variant: 'info' as 'info',
      detail: 'ChromaDB + MiniLM Embeddings',
    },
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((card) => {
        const Icon = card.icon;
        return (
          <Card key={card.title} className="flex flex-col justify-between hover:border-slate-700 transition-colors">
            <div className="flex items-start justify-between">
              <div className="p-2.5 rounded-lg bg-slate-800/80 border border-slate-700/50 text-slate-300">
                <Icon className="h-5 w-5" />
              </div>
              <Badge variant={card.variant}>{card.status}</Badge>
            </div>
            <div className="mt-4">
              <h3 className="text-sm font-semibold text-slate-200">{card.title}</h3>
              <p className="text-xs text-slate-500 mt-0.5">{card.subtitle}</p>
              <div className="mt-3 pt-3 border-t border-slate-800 text-[11px] font-mono text-slate-400">
                {card.detail}
              </div>
            </div>
          </Card>
        );
      })}
    </div>
  );
};
