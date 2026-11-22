import React from 'react';
import { Card } from '../ui/Card';
import { Badge } from '../ui/Badge';
import { Button } from '../ui/Button';
import { FileText, Trash2 } from 'lucide-react';
import { useDocuments } from '../../hooks/useDocuments';

export const DocumentList: React.FC = () => {
  const { documents, remove, isLoading } = useDocuments();

  if (documents.length === 0) {
    return (
      <Card className="p-8 text-center text-slate-500 border-dashed border-slate-800">
        <FileText className="h-8 w-8 mx-auto mb-2 opacity-50" />
        <p className="text-sm">No documents in knowledge base.</p>
        <p className="text-xs text-slate-600 mt-1">
          Upload your resume, system design notes, or project documentation.
        </p>
      </Card>
    );
  }

  return (
    <div className="space-y-3">
      {documents.map((doc) => (
        <Card
          key={doc.id}
          className="p-4 flex items-center justify-between bg-slate-900 border-slate-800 hover:border-slate-700/80 transition-colors"
        >
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-slate-800 text-emerald-400">
              <FileText className="h-5 w-5" />
            </div>
            <div>
              <h4 className="text-sm font-medium text-slate-200">{doc.filename}</h4>
              <div className="flex items-center gap-3 text-xs text-slate-500 mt-1 font-mono">
                <span>{(doc.fileSize / 1024).toFixed(1)} KB</span>
                <span>•</span>
                <span>{doc.chunkCount} Vector Chunks</span>
                <span>•</span>
                <span>{new Date(doc.uploadedAt).toLocaleDateString()}</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <Badge variant={doc.status === 'indexed' ? 'success' : 'warning'}>
              {doc.status}
            </Badge>

            <Button
              variant="ghost"
              size="sm"
              onClick={() => remove(doc.id)}
              disabled={isLoading}
              className="text-slate-500 hover:text-rose-400"
            >
              <Trash2 className="h-4 w-4" />
            </Button>
          </div>
        </Card>
      ))}
    </div>
  );
};
