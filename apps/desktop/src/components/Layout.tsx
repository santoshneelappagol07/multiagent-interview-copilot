import React from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-950 text-slate-100 font-sans">
      <Sidebar />
      <div className="flex flex-col flex-1 h-full min-w-0">
        <Header />
        <main className="flex-1 overflow-y-auto p-6 bg-slate-950/50">
          {children}
        </main>
      </div>
    </div>
  );
};
