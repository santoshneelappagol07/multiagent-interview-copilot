import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { Layout } from './components/Layout';
import { Dashboard } from './pages/Dashboard';
import { Transcription } from './pages/Transcription';
import { AIPanel } from './pages/AIPanel';
import { Documents } from './pages/Documents';
import { Settings } from './pages/Settings';
import { useWebSocket } from './hooks/useWebSocket';

export const AppContent: React.FC = () => {
  // Initialize continuous WebSocket connection to Python backend
  useWebSocket();

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/transcription" element={<Transcription />} />
        <Route path="/ai" element={<AIPanel />} />
        <Route path="/documents" element={<Documents />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Layout>
  );
};

export const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Toaster
        position="top-right"
        toastOptions={{
          style: {
            background: '#0f172a',
            color: '#f8fafc',
            border: '1px solid #1e293b',
            fontSize: '13px',
          },
        }}
      />
      <AppContent />
    </BrowserRouter>
  );
};

export default App;
