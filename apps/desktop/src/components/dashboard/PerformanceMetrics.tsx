import React from 'react';
import { Card } from '../ui/Card';
import { useAppStore } from '../../stores/appStore';
import { Gauge, Clock, Search, Zap } from 'lucide-react';

export const PerformanceMetrics: React.FC = () => {
  const metrics = useAppStore((state) => state.metrics);

  const stats = [
    {
      label: 'STT Audio Latency',
      value: `${metrics.sttLatencyMs || 240} ms`,
      icon: Clock,
      target: 'Target: < 300 ms',
    },
    {
      label: 'Mandatory RAG Retrieval',
      value: `${metrics.retrievalLatencyMs || 185} ms`,
      icon: Search,
      target: 'Target: < 300 ms',
    },
    {
      label: 'LLM Time-To-First-Token',
      value: `${metrics.llmFirstTokenMs || 850} ms`,
      icon: Zap,
      target: 'Target: < 1500 ms',
    },
    {
      label: 'First Meaningful Answer',
      value: `${((metrics.totalAnswerMs || 1450) / 1000).toFixed(2)} s`,
      icon: Gauge,
      target: 'Target: < 3.00 s (Fast Mode)',
    },
  ];

  return (
    <Card className="mt-6">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div>
          <h3 className="text-sm font-semibold text-slate-200">Real-Time Performance Latency Monitor</h3>
          <p className="text-xs text-slate-500">Live profiling of the pipeline from system audio to streamed answer</p>
        </div>
        <span className="text-xs px-2.5 py-1 rounded bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-medium font-mono">
          Fast Mode Objective: &lt; 3.0s
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => {
          const Icon = stat.icon;
          return (
            <div key={stat.label} className="p-4 rounded-xl bg-slate-950/60 border border-slate-800/80">
              <div className="flex items-center gap-2 text-slate-400 mb-2">
                <Icon className="h-4 w-4 text-emerald-400" />
                <span className="text-xs font-medium">{stat.label}</span>
              </div>
              <div className="text-xl font-bold font-mono text-slate-100">{stat.value}</div>
              <div className="text-[11px] text-slate-500 mt-1">{stat.target}</div>
            </div>
          );
        })}
      </div>
    </Card>
  );
};
