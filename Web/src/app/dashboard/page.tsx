"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function DashboardOverviewPage() {
  const [user, setUser] = useState<any>(null);

  useEffect(() => {
    api.get("/users/me").then((res) => setUser(res.data)).catch(() => {});
  }, []);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">System Overview</h1>
        <p className="text-sm text-slate-400 mt-1">
          Welcome back, {user?.full_name || "User"}. Here is your portal activity summary.
        </p>
      </div>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
          <p className="text-xs uppercase text-slate-400 font-semibold tracking-wider">Role Access</p>
          <p className="text-xl font-bold text-blue-400 mt-2">{user?.role || "EMPLOYEE"}</p>
        </div>
        <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
          <p className="text-xs uppercase text-slate-400 font-semibold tracking-wider">Employee ID</p>
          <p className="text-xl font-bold text-slate-200 mt-2">{user?.employee_id || "EX-0001"}</p>
        </div>
        <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
          <p className="text-xs uppercase text-slate-400 font-semibold tracking-wider">Account Status</p>
          <p className="text-xl font-bold text-emerald-400 mt-2">
            {user?.is_active ? "Active" : "Inactive"}
          </p>
        </div>
        <div className="p-5 bg-slate-900 border border-slate-800 rounded-xl">
          <p className="text-xs uppercase text-slate-400 font-semibold tracking-wider">System State</p>
          <p className="text-xl font-bold text-indigo-400 mt-2">Synchronized</p>
        </div>
      </div>
    </div>
  );
}