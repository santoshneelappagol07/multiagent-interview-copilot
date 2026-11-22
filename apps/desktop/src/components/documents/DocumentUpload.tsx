import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Card } from '../ui/Card';
import { UploadCloud, AlertCircle } from 'lucide-react';
import { useDocuments } from '../../hooks/useDocuments';
import toast from 'react-hot-toast';

export const DocumentUpload: React.FC = () => {
  const { upload, isLoading } = useDocuments();

  const onDrop = useCallback(
    async (acceptedFiles: File[]) => {
      for (const file of acceptedFiles) {
        try {
          await upload(file);
          toast.success(`Uploaded and indexed ${file.name}`);
        } catch (e) {
          toast.error(`Failed to process ${file.name}`);
        }
      }
    },
    [upload]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc'],
      'text/plain': ['.txt'],
    },
    disabled: isLoading,
  });

  return (
    <Card
      {...getRootProps()}
      className={`border-2 border-dashed p-8 text-center cursor-pointer transition-colors ${
        isDragActive
          ? 'border-emerald-500 bg-emerald-950/20'
          : 'border-slate-800 hover:border-slate-700 bg-slate-900/40'
      }`}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center justify-center">
        <div className="p-3 rounded-full bg-slate-800 text-slate-300 mb-3">
          <UploadCloud className="h-6 w-6" />
        </div>
        <p className="text-sm font-semibold text-slate-200">
          {isDragActive
            ? 'Drop resume or project documents here...'
            : 'Click or drag files here to upload'}
        </p>
        <p className="text-xs text-slate-500 mt-1">
          Supports PDF, DOCX, DOC, and TXT (Max 50MB)
        </p>
        <div className="flex items-center gap-1.5 mt-3 text-[11px] text-emerald-400 font-medium">
          <AlertCircle className="h-3.5 w-3.5" />
          Mandatory Knowledge Base: Consulted on EVERY answer query
        </div>
      </div>
    </Card>
  );
};
