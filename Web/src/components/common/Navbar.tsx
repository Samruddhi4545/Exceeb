"use client";

import React from "react";
import { User } from "@/types";

interface NavbarProps {
user: User | null;
onLogout: () => void;
}

export const Navbar: React.FC<NavbarProps> = ({ user, onLogout }) => {
return (
    <header className="border-b border-slate-800 bg-slate-900 px-6 py-4 flex items-center justify-between sticky top-0 z-50">
    <div className="flex items-center gap-3">
        <div className="h-8 w-8 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white shadow-md">
        E
        </div>
        <span className="font-bold text-lg text-white tracking-tight">
        EXCEEB System
        </span>
    </div>

    <div className="flex items-center gap-4">
        {user && (
        <div className="text-right text-xs hidden sm:block">
            <p className="font-semibold text-slate-200">
            {user.full_name || user.email}
            </p>
            <p className="text-blue-400 font-mono text-[11px]">{user.role}</p>
        </div>
        )}
        <button
        onClick={onLogout}
        className="rounded-lg bg-red-600/20 text-red-400 hover:bg-red-600/30 border border-red-500/20 px-3.5 py-1.5 text-xs font-semibold transition-all duration-200 active:scale-95"
        >
        Logout
        </button>
    </div>
    </header>
);
};