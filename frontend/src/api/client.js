import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:8000/api"
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("moodtune_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export function apiMessage(error) {
  const detail = error?.response?.data?.detail || error?.message || "Something went wrong";
  return typeof detail === "string" ? detail : detail.message || JSON.stringify(detail);
}
