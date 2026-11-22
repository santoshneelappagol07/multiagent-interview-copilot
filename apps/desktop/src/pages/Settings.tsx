import React, { useState } from 'react';
import { APIKeyManager } from '../components/settings/APIKeyManager';
import { LLMConfig } from '../components/settings/LLMConfig';
import { AudioConfig } from '../components/settings/AudioConfig';
import { Key, Cpu, Volume2 } from 'lucide-react';
import clsx from 'clsx';

export const Settings: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'keys' | 'llm' | 'audio'>('keys');

  const tabs = [
    { id: 'keys', label: 'Free LLM API Keys', icon: Key },
    { id: 'llm', label: 'Model Modes & Routing', icon: Cpu },
    { id: 'audio', label: 'Audio Loopback Capture', icon: Volume2 },
  ];

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div>
        <h2 className="text-base font-semibold text-slate-100">Application Configuration</h2>
        <p className="text-xs text-slate-400 mt-0.5">
          Configure API credentials, automatic routing policies, and system audio loopback settings.
        </p>
      </div>

      <div className="flex items-center gap-2 border-b border-slate-800 pb-2">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={clsx(
                'flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-medium transition-colors',
                isActive
                  ? 'bg-slate-800 text-emerald-400 border border-slate-700/60'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-900'
              )}
            >
              <Icon className="h-4 w-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      <div>
        {activeTab === 'keys' && <APIKeyManager />}
        {activeTab === 'llm' && <LLMConfig />}
        {activeTab === 'audio' && <AudioConfig />}
      </div>
    </div>
  );
};
