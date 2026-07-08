import { useEffect, useState } from "react";
import { Activity, Music, Users } from "lucide-react";
import { Bar, BarChart, CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "../api/client";

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  useEffect(() => { api.get("/admin/stats").then((res) => setStats(res.data)); }, []);
  if (!stats) return <div className="panel p-5">Loading admin analytics...</div>;
  return (
    <div className="grid gap-6">
      <section className="grid gap-4 md:grid-cols-4">
        <div className="stat"><Users /><b className="text-2xl">{stats.total_users}</b><span>Total Users</span></div>
        <div className="stat"><Music /><b className="text-2xl">{stats.total_recommendations}</b><span>Total Recommendations</span></div>
        <div className="stat"><Activity /><b className="text-2xl capitalize">{stats.most_detected_emotion}</b><span>Most Detected Emotion</span></div>
        <div className="stat"><b className="text-2xl">{stats.api_statistics.emotion_detections}</b><span>Emotion API Calls</span></div>
      </section>
      <div className="grid gap-6 lg:grid-cols-2">
        <section className="panel p-4"><h2 className="mb-3 font-black">Daily Activity</h2><ResponsiveContainer height={260}><BarChart data={stats.daily_activity}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="date" /><YAxis /><Tooltip /><Bar dataKey="count" fill="#176b87" /></BarChart></ResponsiveContainer></section>
        <section className="panel p-4"><h2 className="mb-3 font-black">Monthly Activity</h2><ResponsiveContainer height={260}><LineChart data={stats.monthly_activity}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="date" /><YAxis /><Tooltip /><Line dataKey="count" stroke="#9a3412" strokeWidth={2} /></LineChart></ResponsiveContainer></section>
      </div>
      <section className="panel overflow-x-auto p-4">
        <h2 className="mb-3 font-black">User Management</h2>
        <table className="w-full min-w-[640px] text-left text-sm">
          <thead><tr className="border-b"><th className="p-2">Name</th><th className="p-2">Email</th><th className="p-2">Role</th><th className="p-2">Joined</th></tr></thead>
          <tbody>{stats.users.map((user) => <tr className="border-b" key={user.id}><td className="p-2 font-bold">{user.name}</td><td className="p-2">{user.email}</td><td className="p-2">{user.role}</td><td className="p-2">{new Date(user.created_at).toLocaleDateString()}</td></tr>)}</tbody>
        </table>
      </section>
    </div>
  );
}
