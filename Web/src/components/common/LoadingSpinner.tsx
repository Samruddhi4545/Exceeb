"use client";

import React from "react";

interface LoadingSpinnerProps {
label?: string;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
label = "Loading...",
}) => {
return (
    <div className="flex flex-col items-center justify-center p-8 gap-3 min-h-[200px]">
    <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent" />
    <p className="text-sm font-medium text-slate-400">{label}</p>
    </div>
);
};