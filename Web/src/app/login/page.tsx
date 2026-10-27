"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";

export default function LoginPage() {
const [email, setEmail] = useState("");
const [password, setPassword] = useState("");
const [error, setError] = useState("");
const [loading, setLoading] = useState(false);
const router = useRouter();

const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
    const formData = new FormData();
    formData.append("username", email);
    formData.append("password", password);

    const response = await api.post("/auth/login", formData, {
        headers: { "Content-Type": "multipart/form-data" },
    });

    localStorage.setItem("token", response.data.access_token);
    router.push("/dashboard");
    } catch (err: any) {
    setError(err.response?.data?.detail || "Invalid email or password.");
    } finally {
    setLoading(false);
    }
};

return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-4">
    <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-xl p-8 shadow-2xl">
        <div className="text-center mb-8">
        <h2 className="text-2xl font-bold text-white">EXCEEB System</h2>
        <p className="text-slate-400 text-sm mt-1">Sign in to your account</p>
        </div>

        {error && (
        <div className="mb-4 p-3 bg-red-500/10 border border-red-500/20 text-red-400 text-sm rounded-lg text-center">
            {error}
        </div>
        )}

        <form onSubmit={handleLogin} className="space-y-4">
        <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Email Address
            </label>
            <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 text-white rounded-lg focus:outline-none focus:border-blue-500"
            placeholder="admin@exceeb.com"
            />
        </div>

        <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Password
            </label>
            <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full px-4 py-2.5 bg-slate-800 border border-slate-700 text-white rounded-lg focus:outline-none focus:border-blue-500"
            placeholder="••••••••"
            />
        </div>

        <button
            type="submit"
            disabled={loading}
            className="w-full py-3 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-lg transition-colors mt-2"
        >
            {loading ? "Authenticating..." : "Sign In"}
        </button>
        </form>
    </div>
    </div>
);
}