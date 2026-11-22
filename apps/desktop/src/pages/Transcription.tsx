import React from 'react';
import { TranscriptView } from '../components/transcript/TranscriptView';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Trash2, Radio } from 'lucide-react';
import { useTranscriptStore } from '../stores/transcriptStore';
import { useAudio } from '../hooks/useAudio';

export const Transcription: React.FC = () => {
  const clearTranscript = useTranscriptStore((state) => state.clearTranscript);
  const { isCapturing, toggleCapture } = useAudio();

  return (
    <div className="space-y-4 max-w-5xl mx-auto">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="h-3 w-3 rounded-full bg-emerald-500 animate-ping" />
          <h2 className="text-base font-semibold text-slate-100">Live Interview Transcript</h2>
          <span className="text-xs text-slate-500 font-mono">Loopback Audio Feed</span>
        </div>

        <div className="flex items-center gap-2">
          <Button
            size="sm"
            variant={isCapturing ? 'danger' : 'primary'}
            onClick={toggleCapture}
            className="flex items-center gap-1.5"
          >
            <Radio className="h-3.5 w-3.5" />
            {isCapturing ? 'Stop Listening' : 'Start Listening'}
          </Button>

          <Button
            size="sm"
            variant="outline"
            onClick={clearTranscript}
            className="flex items-center gap-1.5"
          >
            <Trash2 className="h-3.5 w-3.5" />
            Clear
          </Button>
        </div>
      </div>

      <Card className="min-h-[550px] max-h-[700px] overflow-y-auto p-4 bg-slate-950/70 border-slate-800">
        <TranscriptView />
      </Card>
    </div>
  );
};
