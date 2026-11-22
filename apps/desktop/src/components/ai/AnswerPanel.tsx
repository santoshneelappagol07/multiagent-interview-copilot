import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Copy, Check, FileText } from 'lucide-react';
import { useAnswerStore } from '../../stores/answerStore';
import toast from 'react-hot-toast';

export const AnswerPanel: React.FC = () => {
  const { streamingText, answers, isGenerating, activeSources } = useAnswerStore();
  const [copied, setCopied] = React.useState(false);

  const latestAnswer = answers[0];
  const displayText = isGenerating ? streamingText : latestAnswer?.answer || streamingText;

  const handleCopy = () => {
    if (!displayText) return;
    navigator.clipboard.writeText(displayText);
    setCopied(true);
    toast.success('Answer copied to clipboard');
    setTimeout(() => setCopied(false), 2000);
  };

  if (!displayText && !isGenerating) {
    return (
      <Card className="min-h-[350px] flex flex-col items-center justify-center text-slate-500 border-dashed border-slate-800">
        <FileText className="h-8 w-8 mb-2 opacity-50 text-slate-400" />
        <p className="text-sm">No answer generated yet.</p>
        <p className="text-xs text-slate-600 mt-1">
          Select or enter an interview question above and click Generate Answer.
        </p>
      </Card>
    );
  }

  return (
    <Card className="min-h-[400px] flex flex-col justify-between bg-slate-900/90 border-slate-800">
      <div>
        <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wide">
              {isGenerating ? 'Streaming Answer...' : 'Generated Interview Response'}
            </span>
            {latestAnswer && (
              <>
                <Badge variant="info">
                  {latestAnswer.provider.toUpperCase()} • {latestAnswer.latencyMs}ms
                </Badge>
                {latestAnswer.contextCarriedCount ? (
                  <Badge variant="success">
                    {latestAnswer.contextCarriedCount} Prior Q&A Linked
                  </Badge>
                ) : null}
              </>
            )}
          </div>

          <button
            type="button"
            onClick={handleCopy}
            className="flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-xs text-slate-300 transition-colors"
          >
            {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
            {copied ? 'Copied' : 'Copy'}
          </button>
        </div>

        <div className="prose prose-invert prose-sm max-w-none text-slate-200 leading-relaxed space-y-3 font-normal">
          <ReactMarkdown remarkPlugins={[remarkGfm]}>{displayText}</ReactMarkdown>
        </div>
      </div>

      {activeSources.length > 0 && (
        <div className="mt-6 pt-4 border-t border-slate-800/80">
          <div className="text-xs font-semibold text-slate-400 mb-2 flex items-center gap-1.5">
            <FileText className="h-3.5 w-3.5 text-emerald-400" />
            Mandatory RAG Sources Consulted:
          </div>
          <div className="flex flex-wrap gap-2">
            {activeSources.map((source, idx) => (
              <span
                key={idx}
                className="text-[11px] px-2 py-0.5 rounded bg-slate-950 border border-slate-800 text-slate-300 font-mono"
              >
                {source}
              </span>
            ))}
          </div>
        </div>
      )}
    </Card>
  );
};
