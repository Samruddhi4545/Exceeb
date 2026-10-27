"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function HomePage() {
const router = useRouter();

useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
    router.replace("/dashboard");
    } else {
    router.replace("/login");
    }
}, [router]);

return (
    <div className="flex min-h-screen items-center justify-center bg-slate-950">
    <div className="flex flex-col items-center gap-3">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-500 border-t-transparent" />
        <p className="text-sm text-slate-400 font-medium">Initializing EXCEEB Portal...</p>
    </div>
    </div>
);
}