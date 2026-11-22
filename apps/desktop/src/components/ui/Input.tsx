import React from 'react';
import clsx from 'clsx';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input: React.FC<InputProps> = ({ label, error, className, ...props }) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-xs font-medium text-slate-400 mb-1">
          {label}
        </label>
      )}
      <input
        className={clsx(
          'w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 placeholder-slate-600 focus:outline-none focus:ring-2 focus:ring-emerald-500 focus:border-transparent transition-all',
          error && 'border-rose-500 focus:ring-rose-500',
          className
        )}
        {...props}
      />
      {error && <p className="mt-1 text-xs text-rose-400">{error}</p>}
    </div>
  );
};
