import { useEffect } from 'react';
import { api } from '../services/api';
import { useDocumentStore } from '../stores/documentStore';

export function useDocuments() {
  const { documents, isLoading, setDocuments, addDocument, removeDocument, setLoading } =
    useDocumentStore();

  const loadDocuments = async () => {
    try {
      setLoading(true);
      const docs = await api.listDocuments();
      setDocuments(docs);
    } catch (err) {
      console.error('Failed to load documents:', err);
    } finally {
      setLoading(false);
    }
  };

  const upload = async (file: File) => {
    try {
      setLoading(true);
      const newDoc = await api.uploadDocument(file);
      addDocument(newDoc);
    } catch (err) {
      console.error('Upload failed:', err);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const remove = async (id: string) => {
    try {
      await api.deleteDocument(id);
      removeDocument(id);
    } catch (err) {
      console.error('Delete failed:', err);
    }
  };

  useEffect(() => {
    loadDocuments();
  }, []);

  return { documents, isLoading, upload, remove, refresh: loadDocuments };
}
