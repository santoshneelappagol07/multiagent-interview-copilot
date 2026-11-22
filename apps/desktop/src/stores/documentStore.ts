import { create } from 'zustand';
import { DocumentItem } from '../types';

interface DocumentState {
  documents: DocumentItem[];
  isLoading: boolean;
  setDocuments: (docs: DocumentItem[]) => void;
  addDocument: (doc: DocumentItem) => void;
  removeDocument: (id: string) => void;
  setLoading: (loading: boolean) => void;
}

export const useDocumentStore = create<DocumentState>((set) => ({
  documents: [],
  isLoading: false,
  setDocuments: (documents) => set({ documents }),
  addDocument: (doc) => set((state) => ({ documents: [doc, ...state.documents] })),
  removeDocument: (id) =>
    set((state) => ({ documents: state.documents.filter((d) => d.id !== id) })),
  setLoading: (isLoading) => set({ isLoading }),
}));
