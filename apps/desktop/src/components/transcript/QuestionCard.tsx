import React from 'react';
import { Card } from '../ui/Card';
import { Button } from '../ui/Button';
import { Sparkles, HelpCircle } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useTranscriptStore } from '../../stores/transcriptStore';

interface QuestionCardProps {
  question: string;
  timestamp: number;
}

export const QuestionCard: React.FC<QuestionCardProps> = ({ question, timestamp }) => {
  const navigate = useNavigate();
  const setSelectedQuestion = useTranscriptStore((state) => state.setSelectedQuestion);

  const handleGenerate = () => {
    setSelectedQuestion(question);
    navigate('/ai');
  };

  return (
    <Card className="bg-emerald-950/20 border-emerald-500/30 p-4 hover:border-emerald-500/50 transition-colors">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-2.5">
          <HelpCircle className="h-4 w-4 text-emerald-400 mt-0.5 flex-shrink-0" />
          <div>
            <div className="text-xs font-semibold text-emerald-400 uppercase tracking-wide">
              Detected Interviewer Question
            </div>
            <p className="text-sm font-medium text-slate-100 mt-1">{question}</p>
            <span className="text-[11px] text-slate-500 font-mono mt-1 block">
              {new Date(timestamp).toLocaleTimeString()}
            </span>
          </div>
        </div>

        <Button
          size="sm"
          variant="primary"
          onClick={handleGenerate}
          className="flex-shrink-0 flex items-center gap-1.5 shadow-sm"
        >
          <Sparkles className="h-3.5 w-3.5" />
          Generate Answer
        </Button>
      </div>
    </Card>
  );
};
