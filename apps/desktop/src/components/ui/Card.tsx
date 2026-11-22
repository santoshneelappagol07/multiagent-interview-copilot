import React from 'react';
import clsx from 'clsx';

export const Card: React.FC<React.HTMLAttributes<HTMLDivElement>> = ({
  children,
  className,
  ...props
}) => {
  return (
    <div
      className={clsx(
        'bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
