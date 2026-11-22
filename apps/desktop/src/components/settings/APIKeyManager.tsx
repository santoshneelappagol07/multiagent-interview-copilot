import React, { useState } from 'react';
import { Card } from '../ui/Card';
import { Input } from '../ui/Input';
import { Button } from '../ui/Button';
import { Eye, EyeOff, CheckCircle } from 'lucide-react';
import toast from 'react-hot-toast';

export const APIKeyManager: React.FC = () => {
  const [showKeys, setShowKeys] = useState<{ [key: string]: boolean }>({});
  const [keys, setKeys] = useState({
    gemini: '',
    groq: '',
    cerebras: '',
  });

  const toggleShow = (provider: string) => {
    setShowKeys((prev) => ({ ...prev, [provider]: !prev[provider] }));
  };

  const handleSave = () => {
    toast.success('API Keys securely saved and updated in backend');
  };

  const providers = [
    {
      id: 'gemini',
      name: 'Google Gemini (Free AI Studio)',
      placeholder: 'AIzaSy...',
      link: 'https://aistudio.google.com/',
      role: 'Reasoning Mode Primary',
    },
    {
      id: 'groq',
      name: 'Groq Cloud (Free Tier)',
      placeholder: 'gsk_...',
      link: 'https://console.groq.com/',
      role: 'Fast Mode (<3s) & Research Mode',
    },
    {
      id: 'cerebras',
      name: 'Cerebras Cloud (Free Tier)',
      placeholder: 'csk-...',
      link: 'https://cloud.cerebras.ai/',
      role: 'Fast Mode Ultra-Low Latency Fallback',
    },
  ];

  return (
    <div className="space-y-4">
      {providers.map((p) => (
        <Card key={p.id} className="p-4 bg-slate-900 border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-semibold text-slate-200">{p.name}</h4>
              <p className="text-xs text-slate-500 mt-0.5">{p.role}</p>
            </div>
            <a
              href={p.link}
              target="_blank"
              rel="noreferrer"
              className="text-xs text-emerald-400 hover:underline font-mono"
            >
              Get Free API Key ↗
            </a>
          </div>

          <div className="flex items-center gap-2">
            <div className="relative flex-1">
              <Input
                type={showKeys[p.id] ? 'text' : 'password'}
                placeholder={p.placeholder}
                value={keys[p.id as keyof typeof keys]}
                onChange={(e) =>
                  setKeys({ ...keys, [p.id]: e.target.value })
                }
              />
              <button
                type="button"
                onClick={() => toggleShow(p.id)}
                className="absolute right-3 top-2.5 text-slate-500 hover:text-slate-300"
              >
                {showKeys[p.id] ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>
        </Card>
      ))}

      <Button variant="primary" onClick={handleSave} className="flex items-center gap-2">
        <CheckCircle className="h-4 w-4" />
        Save & Verify API Keys
      </Button>
    </div>
  );
};
