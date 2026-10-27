import axios from "axios";

export const api = axios.create({
baseURL: process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8001/api/v1",
headers: {
    "Content-Type": "application/json",
},
});

// Interceptor to attach JWT token from localStorage to every request
api.interceptors.request.use(
(config) => {
    if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    }
    return config;
},
(error) => Promise.reject(error)
);

// Interceptor to automatically handle 401 Unauthorized token expiries
api.interceptors.response.use(
(response) => response,
(error) => {
    if (
    typeof window !== "undefined" &&
    error.response &&
    error.response.status === 401
    ) {
    localStorage.removeItem("token");
    if (window.location.pathname !== "/login") {
        window.location.href = "/login";
    }
    }
    return Promise.reject(error);
}
);