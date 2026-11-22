import React from 'react';
import { useLocation } from 'react-router-dom';
import { Volume2 } from 'lucide-react';
import { useAppStore } from '../stores/appStore';
import { useAudio } from '../hooks/useAudio';
import { Button } from './ui/Button';

export const Header: React.FC = () => {
  const location = useLocation();
  const { isCapturing, toggleCapture } = useAudio();
  const answerMode = useAppStore((state) => state.answerMode);

  const getPageTitle = () => {
    switch (location.pathname) {
      case '/':
        return 'Overview Dashboard';
      case '/transcription':
        return 'Live System Audio Transcription';
      case '/ai':
        return 'AI Answer Copilot';
      case '/documents':
        return 'Document Knowledge Base (Mandatory RAG)';
      case '/settings':
        return 'Application & LLM Settings';
      default:
        return 'AI Voice Copilot';
    }
  };

  return (
    <header className="h-16 px-6 bg-slate-900/60 border-b border-slate-800/80 flex items-center justify-between backdrop-blur-md">
      <div className="flex items-center gap-3">
        <h2 className="text-base font-semibold text-slate-100">{getPageTitle()}</h2>
        <span className="text-xs px-2 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700/60 uppercase font-mono">
          {answerMode} mode
        </span>
      </div>

      <div className="flex items-center gap-3">
        <Button
          variant={isCapturing ? 'danger' : 'primary'}
          size="sm"
          onClick={toggleCapture}
          className="flex items-center gap-2 shadow-sm"
        >
          <Volume2 className="h-4 w-4" />
          {isCapturing ? 'Stop Audio Capture' : 'Start System Capture'}
        </Button>
      </div>
    </header>
  );
};
