import React, { useState } from 'react';
import { DocumentUpload } from '../components/documents/DocumentUpload';
import { DocumentList } from '../components/documents/DocumentList';
import { BookOpen, ShieldCheck, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import { useDocumentStore } from '../stores/documentStore';
import toast from 'react-hot-toast';

export const Documents: React.FC = () => {
  const [reindexing, setReindexing] = useState(false);
  const setDocuments = useDocumentStore((state) => state.setDocuments);

  const handleReindex = async () => {
    try {
      setReindexing(true);
      const res = await api.reindexDocuments();
      toast.success(`Successfully indexed ${res.filesProcessed} knowledge base files!`);
      const docs = await api.listDocuments();
      setDocuments(docs);
    } catch (err: any) {
      toast.error(err.message || 'Re-indexing failed');
    } finally {
      setReindexing(false);
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="flex items-start justify-between pb-4 border-b border-slate-800">
        <div>
          <h2 className="text-base font-semibold text-slate-100">Document Knowledge Base</h2>
          <p className="text-xs text-slate-400 mt-0.5">
            Files uploaded or stored in originals are chunked, normalized, and embedded into local ChromaDB for mandatory RAG.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            type="button"
            onClick={handleReindex}
            disabled={reindexing}
            className="flex items-center gap-1.5 text-xs font-medium text-slate-300 bg-slate-800 hover:bg-slate-700 border border-slate-700 px-3 py-1.5 rounded-lg transition-colors disabled:opacity-50"
            title="Scan storage/documents/originals and index all candidate transcripts"
          >
            <RefreshCw className={`h-3.5 w-3.5 text-emerald-400 ${reindexing ? 'animate-spin' : ''}`} />
            {reindexing ? 'Re-indexing...' : 'Re-index Knowledge Base'}
          </button>

          <div className="flex items-center gap-2 text-xs font-medium text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-3 py-1.5 rounded-lg">
            <ShieldCheck className="h-4 w-4" />
            100% Local Storage
          </div>
        </div>
      </div>

      {/* Upload Box */}
      <DocumentUpload />

      {/* Uploaded Documents List */}
      <div>
        <h3 className="text-xs font-semibold text-slate-400 uppercase tracking-wide mb-3 flex items-center gap-2">
          <BookOpen className="h-4 w-4 text-emerald-400" />
          Indexed Knowledge Documents
        </h3>
        <DocumentList />
      </div>
    </div>
  );
};
