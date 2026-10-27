export enum UserRole {
MAIN_ADMIN = "MAIN_ADMIN",
ADMIN = "ADMIN",
SUPERVISOR = "SUPERVISOR",
MANAGER = "MANAGER",
EMPLOYEE = "EMPLOYEE",
}

export interface User {
id: number;
email: string;
full_name: string;
role: UserRole;
employee_id?: string | null;
is_active: boolean;
department_id?: number | null;
team_id?: number | null;
created_at?: string;
}

export interface Department {
id: number;
name: string;
code: string;
description?: string | null;
created_at: string;
}

export interface Team {
id: number;
name: string;
department_id: number;
manager_id?: number | null;
created_at: string;
}

export interface Task {
id: number;
title: string;
description?: string | null;
status: "PENDING" | "IN_PROGRESS" | "COMPLETED" | "CANCELLED";
priority: "LOW" | "MEDIUM" | "HIGH" | "URGENT";
department_id?: number | null;
assigned_to_id?: number | null;
created_by_id?: number | null;
created_at: string;
}

export interface WorkSession {
id: number;
user_id: number;
session_start: string;
session_end?: string | null;
is_active: boolean;
}