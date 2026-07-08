import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { api } from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(localStorage.getItem("moodtune_token")));

  useEffect(() => {
    const token = localStorage.getItem("moodtune_token");
    if (!token) return;
    api.get("/auth/me").then((res) => setUser(res.data)).catch(() => localStorage.removeItem("moodtune_token")).finally(() => setLoading(false));
  }, []);

  const value = useMemo(() => ({
    user,
    loading,
    async login(payload) {
      const { data } = await api.post("/auth/login", payload);
      localStorage.setItem("moodtune_token", data.access_token);
      setUser(data.user);
    },
    async register(payload) {
      const { data } = await api.post("/auth/register", payload);
      localStorage.setItem("moodtune_token", data.access_token);
      setUser(data.user);
    },
    logout() {
      localStorage.removeItem("moodtune_token");
      setUser(null);
    },
    setUser
  }), [user, loading]);

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
