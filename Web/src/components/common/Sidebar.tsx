"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { UserRole } from "@/types";

interface NavItem {
  label: string;
  href: string;
  roles?: UserRole[];
}

export const Sidebar: React.FC = () => {
  const pathname = usePathname();
  const { user } = useAuth();

  const navItems: NavItem[] = [
    { label: "Overview", href: "/dashboard" },
    {
      label: "Departments",
      href: "/dashboard/departments",
      roles: [UserRole.MAIN_ADMIN, UserRole.ADMIN],
    },
    {
      label: "Teams",
      href: "/dashboard/teams",
      roles: [UserRole.MAIN_ADMIN, UserRole.ADMIN, UserRole.SUPERVISOR, UserRole.MANAGER],
    },
    { label: "Tasks", href: "/dashboard/tasks" },
    { label: "Tracking", href: "/dashboard/tracking" },
  ];

  const visibleNavItems = navItems.filter((item) => {
    if (!item.roles) return true;
    return user && item.roles.includes(user.role);
  });

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-900/50 p-4 hidden md:block min-h-[calc(100vh-65px)]">
      <nav className="space-y-1">
        {visibleNavItems.map((item) => {
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