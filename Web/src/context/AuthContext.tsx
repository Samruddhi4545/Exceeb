"use client";

import React, { createContext, useContext, useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import { User } from "@/types";

interface AuthContextType {
user: User | null;
loading: boolean;
isAuthenticated: boolean;
login: (token: string) => Promise<void>;
logout: () => void;
refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
children,
}) => {
const [user, setUser] = useState<User | null>(null);
const [loading, setLoading] = useState<boolean>(true);
const router = useRouter();

const fetchCurrentUser = async () => {
    try {
    const response = await api.get<User>("/users/me");
    setUser(response.data);
    } catch (error) {
    console.error("Session verification failed:", error);
    setUser(null);
    localStorage.removeItem("token");
    } finally {
    setLoading(false);
    }
};

useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
    fetchCurrentUser();
    } else {
    setLoading(false);
    }
}, []);

const login = async (token: string) => {
    localStorage.setItem("token", token);
    setLoading(true);
    await fetchCurrentUser();
    router.push("/dashboard");
};

const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
    router.push("/login");
};

return (
    <AuthContext.Provider
    value={{
        user,
        loading,
        isAuthenticated: !!user,
        login,
        logout,
        refreshUser: fetchCurrentUser,
    }}
    >
    {children}
    </AuthContext.Provider>
);
};

export const useAuth = (): AuthContextType => {
const context = useContext(AuthContext);
if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
}
return context;
};