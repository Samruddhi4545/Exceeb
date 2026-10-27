"use client";

import React, { useEffect, useState } from "react";
import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { api } from "@/lib/api";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const pathname = usePathname();
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }

    api
      .get("/users/me")
      .then((res) => {
        setUser(res.data);
        setLoading(false);
      })
      .catch(() => {
        localStorage.removeItem("token");
        router.push("/login");
      });
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.push("/login");
  };

  if (loading) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-slate-950 text-white">
        <p className="text-slate-400 font-medium">Loading EXCEEB Portal...</p>
      </div>
    );
  }

  const navItems = [
    { label: "Overview", href: "/dashboard" },
    { label: "Departments", href: "/dashboard/departments" },
    { label: "Teams", href: "/dashboard/teams" },
    { label: "Tasks", href: "/dashboard/tasks" },
    { label: "Tracking", href: "/dashboard/tracking" },
  ];

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
      {/* Navbar */}
      <header className="border-b border-slate-800 bg-slate-900 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-8 w-8 rounded-lg bg-blue-600 flex items-center justify-center font-bold text-white">
            E
          </div>
          <span className="font-bold text-lg text-white">EXCEEB Portal</span>
        </div>
        <div className="flex items-center gap-4">
          <div className="text-right text-xs">
            <p className="font-semibold text-slate-200">{user?.full_name || user?.email}</p>
            <p className="text-blue-400">{user?.role}</p>
          </div>
          <button
            onClick={handleLogout}
            className="rounded-lg bg-red-600/20 text-red-400 hover:bg-red-600/30 px-3 py-1.5 text-xs font-semibold transition-colors"
          >
            Logout
          </button>
        </div>
      </header>

      {/* App Body */}
      <div className="flex flex-1">
        {/* Sidebar */}
        <aside className="w-64 border-r border-slate-800 bg-slate-900/50 p-4 hidden md:block">
          <nav className="space-y-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`block px-4 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? "bg-blue-600 text-white"
                      : "text-slate-400 hover:bg-slate-800 hover:text-slate-200"
                  }`}
                >
                  {item.label}
                </Link>
              );
            })}
          </nav>
        </aside>

        {/* Main View Area */}
        <main className="flex-1 p-6 lg:p-8">{children}</main>
      </div>
    </div>
  );
}