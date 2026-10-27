"use client";

import React from "react";

interface CardProps {
  children: React.ReactNode;
  title?: string;
  subtitle?: string;
  className?: string;
}

export const Card: React.FC<CardProps> = ({
  children,
  title,
  subtitle,
  className = "",
}) => {
  return (
    <div
      className={`bg-slate-900 border border-slate-800 rounded-xl p-6 shadow-xl ${className}`}
    >
      {(title || subtitle) && (
        <div className="mb-4">
          {title && <h3 className="text-lg font-bold text-white">{title}</h3>}
          {subtitle && (
            <p className="text-xs text-slate-400 mt-1">{subtitle}</p>
          )}
        </div>
      )}
      {children}
    </div>
  );
};