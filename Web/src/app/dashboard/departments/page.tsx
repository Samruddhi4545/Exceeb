"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export default function DepartmentsPage() {
const [departments, setDepartments] = useState<any[]>([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
    api
    .get("/departments/")
    .then((res) => {
        setDepartments(res.data);
        setLoading(false);
    })
    .catch(() => setLoading(false));
}, []);

return (
    <div className="space-y-6">
    <div className="flex items-center justify-between">
        <div>
        <h1 className="text-2xl font-bold text-white">Departments</h1>
        <p className="text-sm text-slate-400 mt-1">Manage organizational units and structures.</p>
        </div>
    </div>

    <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
        {loading ? (
        <div className="p-8 text-center text-slate-400">Loading departments...</div>
        ) : departments.length === 0 ? (
        <div className="p-8 text-center text-slate-500">No departments configured yet.</div>
        ) : (
        <table className="w-full text-left text-sm text-slate-300">
            <thead className="bg-slate-950 text-slate-400 text-xs uppercase tracking-wider border-b border-slate-800">
            <tr>
                <th className="p-4">Code</th>
                <th className="p-4">Name</th>
                <th className="p-4">Description</th>
            </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
            {departments.map((dept) => (
                <tr key={dept.id} className="hover:bg-slate-800/50">
                <td className="p-4 font-mono text-blue-400">{dept.code}</td>
                <td className="p-4 font-semibold text-slate-200">{dept.name}</td>
                <td className="p-4 text-slate-400">{dept.description || "N/A"}</td>
                </tr>
            ))}
            </tbody>
        </table>
        )}
    </div>
    </div>
);
}