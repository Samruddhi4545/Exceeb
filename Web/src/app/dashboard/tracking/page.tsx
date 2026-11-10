"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@/context/AuthContext";
import { api } from "@/lib/api";

export default function TrackingPage() {
  const { user } = useAuth();
  const [activeSession, setActiveSession] = useState<boolean>(false);
  const [sessionId, setSessionId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!user) return;

    api
      .get("/tracking/session/active")
      .then((res) => {
        if (res.data.active) {
          setActiveSession(true);
          setSessionId(res.data.session_id);
        }
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, [user]);

  const handleStartSession = async () => {
    try {
      const res = await api.post("/tracking/session/start", { notes: "Web Dashboard Session" });
      setActiveSession(true);
      setSessionId(res.data.work_session_id);
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to start session.");
    }
  };

  const handleEndSession = async () => {
    try {
      await api.post("/tracking/session/end");
      setActiveSession(false);
      setSessionId(null);
    } catch (err: any) {
      alert(err.response?.data?.detail || "Failed to end session.");
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white">Work Session Tracking</h1>
        <p className="text-sm text-slate-400 mt-1">
          Monitor your active shift timer and automatic attendance logging.
        </p>
      </div>

      <div className="p-8 bg-slate-900 border border-slate-800 rounded-xl flex flex-col items-center justify-center space-y-4">
        {loading ? (
          <div className="text-slate-400">Loading session status...</div>
        ) : (
          <>
            <div className="flex items-center space-x-3">
              <span
                className={`h-4 w-4 rounded-full ${
                  activeSession ? "bg-emerald-500 animate-pulse" : "bg-slate-600"
                }`}
              />
              <span className="text-lg font-semibold text-white">
                {activeSession ? `Active Session (#${sessionId})` : "No Active Work Session"}
              </span>
            </div>

            {activeSession ? (
              <button
                onClick={handleEndSession}
                className="px-6 py-2.5 bg-red-600 hover:bg-red-500 text-white rounded-lg text-sm font-semibold transition-colors shadow-lg shadow-red-600/20"
              >
                End Work Session
              </button>
            ) : (
              <button
                onClick={handleStartSession}
                className="px-6 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-lg text-sm font-semibold transition-colors shadow-lg shadow-emerald-600/20"
              >
                Start Work Session
              </button>
            )}
          </>
        )}
      </div>
    </div>
  );
}