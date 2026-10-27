"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function TasksPage() {
const [tasks, setTasks] = useState<any[]>([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
    api
    .get("/tasks/")
    .then((res) => {
        setTasks(res.data);
        setLoading(false);
    })
    .catch(() => setLoading(false));
}, []);

return (
    <div className="space-y-6">
    <div>
        <h1 className="text-2xl font-bold text-white">Tasks</h1>
        <p className="text-sm text-slate-400 mt-1">Operational task assignments and progress.</p>
    </div>

    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        {loading ? (
        <div className="p-8 text-center text-slate-400">Loading tasks...</div>
        ) : tasks.length === 0 ? (
        <div className="p-8 text-center text-slate-500">No tasks assigned.</div>
        ) : (
        <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase tracking-wider border-b border-slate-800">
            <tr>
                <th className="p-4">Title</th>
                <th className="p-4">Status</th>
                <th className="p-4">Priority</th>
            </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
            {tasks.map((task) => (
                <tr key={task.id} className="hover:bg-slate-800/50">
                <td className="p-4 font-semibold text-slate-200">{task.title}</td>
                <td className="p-4">
                    <span className="px-2.5 py-1 text-xs rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 font-medium">
                    {task.status || "PENDING"}
                    </span>
                </td>
                <td className="p-4 text-slate-400">{task.priority || "MEDIUM"}</td>
                </tr>
            ))}
            </tbody>
        </table>
        )}
    </div>
    </div>
);
}