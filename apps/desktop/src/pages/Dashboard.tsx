import React from 'react';
import { StatusCards } from '../components/dashboard/StatusCards';
import { PerformanceMetrics } from '../components/dashboard/PerformanceMetrics';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Mic, Sparkles, FolderUp } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useAudio } from '../hooks/useAudio';

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const { isCapturing, toggleCapture } = useAudio();

  return (
    <div className="space-y-6">
      {/* Hero Quick-Start Card */}
      <Card className="bg-gradient-to-r from-slate-900 via-slate-900 to-slate-950 border border-slate-800">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-medium mb-3">
              <Sparkles className="h-3.5 w-3.5" />
              System Audio Mode (Interviewer Only)
            </div>
            <h2 className="text-xl font-bold text-slate-100">
              Real-Time AI Voice Assistant & Interview Copilot
            </h2>
            <p className="text-sm text-slate-400 mt-1 max-w-2xl">
              Captures interviewer speech via loopback from your remote session (Getscreen.me) or call,
              matches it against your uploaded resume and projects through mandatory local RAG, and produces
              grounded answers in under 3 seconds.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <Button
              variant={isCapturing ? 'danger' : 'primary'}
              size="lg"
              onClick={toggleCapture}
              className="flex items-center gap-2"
            >
              <Mic className="h-4 w-4" />
              {isCapturing ? 'Stop Capture' : 'Start Audio Capture'}
            </Button>
            <Button
              variant="outline"
              size="lg"
              onClick={() => navigate('/documents')}
              className="flex items-center gap-2"
            >
              <FolderUp className="h-4 w-4" />
              Knowledge Base
            </Button>
          </div>
        </div>
      </Card>

      {/* Real-Time Components Status */}
      <StatusCards />

      {/* Latency HUD */}
      <PerformanceMetrics />
    </div>
  );
};
