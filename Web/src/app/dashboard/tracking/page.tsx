"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function TrackingPage() {
const [sessions, setSessions] = useState<any[]>([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
    api
    .get("/tracking/")
    .then((res) => {
        setSessions(res.data);
        setLoading(false);
    })
    .catch(() => setLoading(false));
}, []);

return (
    <div className="space-y-6">
    <div>
        <h1 className="text-2xl font-bold text-white">Work Tracking</h1>
        <p className="text-sm text-slate-400 mt-1">Live work session logs and attendance data.</p>
    </div>

    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden p-6">
        {loading ? (
        <div className="text-center text-slate-400">Loading tracking sessions...</div>
        ) : sessions.length === 0 ? (
        <div className="text-center text-slate-500">No active tracking records available.</div>
        ) : (
        <div className="space-y-3">
            {sessions.map((session) => (
            <div key={session.id} className="p-4 bg-slate-950 border border-slate-800 rounded-lg flex items-center justify-between">
                <div>
                <p className="font-semibold text-slate-200">Session #{session.id}</p>
                <p className="text-xs text-slate-500">{session.created_at}</p>
                </div>
                <span className="text-xs font-semibold px-2.5 py-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-md">
                Active
                </span>
            </div>
            ))}
        </div>
        )}
    </div>
    </div>
);
}