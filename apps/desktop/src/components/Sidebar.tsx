import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Mic, Sparkles, FolderArchive, Settings } from 'lucide-react';
import clsx from 'clsx';
import { useAppStore } from '../stores/appStore';

export const Sidebar: React.FC = () => {
  const isCapturing = useAppStore((state) => state.isCapturing);
  const wsConnected = useAppStore((state) => state.wsConnected);

  const links = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/transcription', label: 'Live Transcript', icon: Mic },
    { to: '/ai', label: 'AI Answer Panel', icon: Sparkles },
    { to: '/documents', label: 'Knowledge Base', icon: FolderArchive },
    { to: '/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 h-full bg-slate-900 border-r border-slate-800 flex flex-col justify-between p-4">
      <div>
        <div className="flex items-center gap-3 px-2 py-4 mb-4 border-b border-slate-800/60">
          <div className="h-8 w-8 rounded-lg bg-emerald-500/20 flex items-center justify-center text-emerald-400 font-bold border border-emerald-500/30">
            AI
          </div>
          <div>
            <h1 className="text-sm font-semibold tracking-wide text-slate-100">AI Voice Copilot</h1>
            <p className="text-xs text-slate-500">Interview Assistant</p>
          </div>
        </div>

        <nav className="space-y-1">
          {links.map((link) => {
            const Icon = link.icon;
            return (
              <NavLink
                key={link.to}
                to={link.to}
                className={({ isActive }) =>
                  clsx(
                    'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-slate-800 text-emerald-400 border border-slate-700/50'
                      : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
                  )
                }
              >
                <Icon className="h-4 w-4" />
                {link.label}
              </NavLink>
            );
          })}
        </nav>
      </div>

      <div className="p-3 bg-slate-950/60 rounded-xl border border-slate-800/80 space-y-2 text-xs">
        <div className="flex items-center justify-between">
          <span className="text-slate-500">System Audio</span>
          <span
            className={clsx(
              'flex items-center gap-1.5 font-medium',
              isCapturing ? 'text-emerald-400' : 'text-slate-500'
            )}
          >
            <span
              className={clsx(
                'h-2 w-2 rounded-full',
                isCapturing ? 'bg-emerald-400 animate-pulse' : 'bg-slate-600'
              )}
            />
            {isCapturing ? 'Capturing' : 'Idle'}
          </span>
        </div>

        <div className="flex items-center justify-between">
          <span className="text-slate-500">Backend Stream</span>
          <span
            className={clsx(
              'flex items-center gap-1.5 font-medium',
              wsConnected ? 'text-emerald-400' : 'text-rose-400'
            )}
          >
            <span
              className={clsx(
                'h-2 w-2 rounded-full',
                wsConnected ? 'bg-emerald-400' : 'bg-rose-500'
              )}
            />
            {wsConnected ? 'Connected' : 'Disconnected'}
          </span>
        </div>
      </div>
    </aside>
  );
};
