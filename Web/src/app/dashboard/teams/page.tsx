"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function TeamsPage() {
const [teams, setTeams] = useState<any[]>([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
    api
    .get("/teams/")
    .then((res) => {
        setTeams(res.data);
        setLoading(false);
    })
    .catch(() => setLoading(false));
}, []);

return (
    <div className="space-y-6">
    <div>
        <h1 className="text-2xl font-bold text-white">Teams</h1>
        <p className="text-sm text-slate-400 mt-1">Active teams and department divisions.</p>
    </div>

    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        {loading ? (
        <div className="p-8 text-center text-slate-400">Loading teams...</div>
        ) : teams.length === 0 ? (
        <div className="p-8 text-center text-slate-500">No teams found.</div>
        ) : (
        <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase tracking-wider border-b border-slate-800">
            <tr>
                <th className="p-4">ID</th>
                <th className="p-4">Team Name</th>
                <th className="p-4">Department ID</th>
            </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
            {teams.map((team) => (
                <tr key={team.id} className="hover:bg-slate-800/50">
                <td className="p-4 text-slate-500">#{team.id}</td>
                <td className="p-4 font-semibold text-slate-200">{team.name}</td>
                <td className="p-4 text-slate-400">{team.department_id}</td>
                </tr>
            ))}
            </tbody>
        </table>
        )}
    </div>
    </div>
);
}