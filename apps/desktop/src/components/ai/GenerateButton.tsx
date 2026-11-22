import React from 'react';
import { Button } from '../ui/Button';
import { Sparkles } from 'lucide-react';
import { useAnswerStore } from '../../stores/answerStore';

interface GenerateButtonProps {
  onGenerate: () => void;
  disabled?: boolean;
}

export const GenerateButton: React.FC<GenerateButtonProps> = ({ onGenerate, disabled }) => {
  const isGenerating = useAnswerStore((state) => state.isGenerating);

  return (
    <Button
      variant="primary"
      size="lg"
      isLoading={isGenerating}
      disabled={disabled || isGenerating}
      onClick={onGenerate}
      className="w-full py-3.5 flex items-center justify-center gap-2 shadow-lg shadow-emerald-950/30 font-semibold text-sm"
    >
      <Sparkles className="h-4 w-4" />
      {isGenerating ? 'Generating Grounded Answer...' : 'Generate Answer (Mandatory RAG + Context)'}
    </Button>
  );
};
