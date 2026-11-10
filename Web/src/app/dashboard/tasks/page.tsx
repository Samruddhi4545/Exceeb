"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { UserRole } from "@/types";
import { api } from "@/lib/api";

interface Task {
  id: number;
  title: string;
  description?: string;
  department_id: number;
  status: string;
  deadline?: string;
}

export default function TasksPage() {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  const canManage =
    user?.role === UserRole.MAIN_ADMIN ||
    user?.role === UserRole.ADMIN ||
    user?.role === UserRole.SUPERVISOR ||
    user?.role === UserRole.MANAGER;

  useEffect(() => {
    if (!user) return;

    api
      .get("/tasks/")
      .then((res) => {
        setTasks(res.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [user]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Tasks</h1>
          <p className="text-sm text-slate-400 mt-1">
            View assigned work tasks and monitor completion status.
          </p>
        </div>
        {canManage && (
          <button className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-medium transition-colors">
            + New Task
          </button>
        )}
      </div>

      <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        {loading ? (
          <div className="p-8 text-center text-slate-400">Loading tasks...</div>
        ) : tasks.length === 0 ? (
          <div className="p-8 text-center text-slate-500">No tasks assigned yet.</div>
        ) : (
          <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase tracking-wider border-b border-slate-800">
              <tr>
                <th className="p-4">ID</th>
                <th className="p-4">Title</th>
                <th className="p-4">Status</th>
                <th className="p-4">Deadline</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {tasks.map((task) => (
                <tr key={task.id} className="hover:bg-slate-800/50">
                  <td className="p-4 font-mono text-slate-500">#{task.id}</td>
                  <td className="p-4">
                    <div className="font-semibold text-slate-200">{task.title}</div>
                    {task.description && (
                      <div className="text-xs text-slate-400 mt-0.5">{task.description}</div>
                    )}
                  </td>
                  <td className="p-4">
                    <span className="px-2 py-1 text-xs rounded bg-blue-950 text-blue-400 border border-blue-800 font-mono">
                      {task.status}
                    </span>
                  </td>
                  <td className="p-4 text-slate-400">
                    {task.deadline ? new Date(task.deadline).toLocaleDateString() : "No deadline"}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}