import { Link, NavLink, Outlet } from "react-router-dom";
import { BarChart3, Heart, LogOut, Music2, Shield, User } from "lucide-react";
import { useAuth } from "../contexts/AuthContext";

export default function AppShell() {
  const { user, logout } = useAuth();
  const nav = ({ isActive }) => `btn ${isActive ? "btn-primary" : "btn-secondary"}`;
  return (
    <div className="app-page">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-3 px-4 py-3">
          <Link to="/" className="flex items-center gap-2 text-xl font-black text-[#174454]"><Music2 /> MoodTune AI</Link>
          <nav className="flex flex-wrap items-center gap-2">
            <NavLink to="/" className={nav}><BarChart3 size={18} /> Dashboard</NavLink>
            <NavLink to="/profile" className={nav}><User size={18} /> Profile</NavLink>
            {user?.role === "admin" && <NavLink to="/admin" className={nav}><Shield size={18} /> Admin</NavLink>}
            <button className="btn btn-secondary" onClick={logout}><LogOut size={18} /> Logout</button>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-4 py-6"><Outlet /></main>
      <footer className="mx-auto flex max-w-7xl items-center gap-2 px-4 pb-6 text-sm text-slate-500"><Heart size={16} /> Built for emotion-aware listening.</footer>
    </div>
  );
}
