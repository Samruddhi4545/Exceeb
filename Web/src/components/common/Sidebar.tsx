"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";

export const Sidebar: React.FC = () => {
const pathname = usePathname();

const navItems = [
    { label: "Overview", href: "/dashboard" },
    { label: "Departments", href: "/dashboard/departments" },
    { label: "Teams", href: "/dashboard/teams" },
    { label: "Tasks", href: "/dashboard/tasks" },
    { label: "Tracking", href: "/dashboard/tracking" },
];

return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/50 p-4 hidden md:block min-h-[calc(100vh-65px)]">
    <nav className="space-y-1">
        {navItems.map((item) => {
        const isActive = pathname === item.href;
        return (
            <Link
            key={item.href}
            href={item.href}
            className={`block px-4 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 ${
                isActive
                ? "bg-blue-600 text-white shadow-lg shadow-blue-600/20"
                : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
            }`}
            >
            {item.label}
            </Link>
        );
        })}
    </nav>
    </aside>
);
};