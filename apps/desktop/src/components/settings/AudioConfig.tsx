import React from 'react';
import { Card } from '../ui/Card';
import { Radio, CheckCircle2 } from 'lucide-react';
import { useAudio } from '../../hooks/useAudio';
import { Button } from '../ui/Button';

export const AudioConfig: React.FC = () => {
  const { isCapturing, toggleCapture } = useAudio();

  return (
    <div className="space-y-4">
      <Card className="p-4 bg-slate-900 border-slate-800 space-y-3">
        <div className="flex items-center justify-between">
          <div>
            <h4 className="text-sm font-semibold text-slate-200">System Audio Loopback</h4>
            <p className="text-xs text-slate-500 mt-0.5">
              Directly captures whatever the remote session (Getscreen.me) or video call plays on your computer.
            </p>
          </div>
          <div className="flex items-center gap-1.5 text-xs text-emerald-400 font-mono">
            <CheckCircle2 className="h-4 w-4" />
            Microphone Excluded (Interviewer Only)
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 text-xs font-mono">
          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
            <span className="text-slate-500 block mb-1">Architecture</span>
            <span className="text-slate-200">CPAL WASAPI Loopback</span>
          </div>
          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
            <span className="text-slate-500 block mb-1">Sample Rate</span>
            <span className="text-slate-200">16,000 Hz Mono</span>
          </div>
          <div className="p-3 bg-slate-950 rounded-lg border border-slate-800">
            <span className="text-slate-500 block mb-1">Processing Buffer</span>
            <span className="text-slate-200">30 ms Sliding Window</span>
          </div>
        </div>

        <div className="pt-2">
          <Button
            variant={isCapturing ? 'danger' : 'primary'}
            size="sm"
            onClick={toggleCapture}
            className="flex items-center gap-2"
          >
            <Radio className="h-4 w-4" />
            {isCapturing ? 'Stop System Audio Capture' : 'Start System Audio Capture'}
          </Button>
        </div>
      </Card>
    </div>
  );
};
