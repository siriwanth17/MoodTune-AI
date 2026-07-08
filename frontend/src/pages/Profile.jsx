import { useState } from "react";
import { Save, Upload } from "lucide-react";
import { api, apiMessage } from "../api/client";
import { useAuth } from "../contexts/AuthContext";

export default function Profile() {
  const { user, setUser } = useAuth();
  const [form, setForm] = useState({ name: user?.name || "", favourite_genres: (user?.favourite_genres || []).join(", ") });
  const [passwords, setPasswords] = useState({ current_password: "", new_password: "" });
  const [message, setMessage] = useState("");

  async function saveProfile(event) {
    event.preventDefault();
    try {
      const { data } = await api.patch("/auth/profile", { name: form.name, favourite_genres: form.favourite_genres.split(",").map((x) => x.trim()).filter(Boolean) });
      setUser(data);
      setMessage("Profile updated");
    } catch (err) {
      setMessage(apiMessage(err));
    }
  }

  async function changePassword(event) {
    event.preventDefault();
    try {
      await api.post("/auth/change-password", passwords);
      setPasswords({ current_password: "", new_password: "" });
      setMessage("Password changed");
    } catch (err) {
      setMessage(apiMessage(err));
    }
  }

  async function upload(event) {
    const file = event.target.files?.[0];
    if (!file) return;
    const body = new FormData();
    body.append("file", file);
    const { data } = await api.post("/auth/profile-picture", body);
    setUser({ ...user, profile_picture: data.profile_picture });
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[320px_1fr]">
      <section className="panel grid content-start gap-4 p-5">
        <img className="aspect-square w-36 rounded-full object-cover" src={user?.profile_picture || "https://images.unsplash.com/photo-1527980965255-d3b416303d12?w=400"} alt="" />
        <div><h1 className="text-2xl font-black">{user?.name}</h1><p className="text-slate-600">{user?.email}</p></div>
        <label className="btn btn-secondary cursor-pointer"><Upload size={18} /> Upload Picture<input className="hidden" type="file" accept="image/*" onChange={upload} /></label>
      </section>
      <section className="panel p-5">
        {message && <p className="mb-4 rounded-md bg-emerald-50 p-3 text-sm text-emerald-800">{message}</p>}
        <form className="grid gap-4" onSubmit={saveProfile}>
          <h2 className="text-xl font-black">Profile</h2>
          <label className="grid gap-1"><span className="label">Name</span><input className="input" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></label>
          <label className="grid gap-1"><span className="label">Favourite genres</span><input className="input" value={form.favourite_genres} onChange={(e) => setForm({ ...form, favourite_genres: e.target.value })} /></label>
          <button className="btn btn-primary w-fit" type="submit"><Save size={18} /> Save Profile</button>
        </form>
        <form className="mt-8 grid gap-4 border-t border-slate-200 pt-6" onSubmit={changePassword}>
          <h2 className="text-xl font-black">Change Password</h2>
          <label className="grid gap-1"><span className="label">Current password</span><input className="input" type="password" value={passwords.current_password} onChange={(e) => setPasswords({ ...passwords, current_password: e.target.value })} /></label>
          <label className="grid gap-1"><span className="label">New password</span><input className="input" type="password" minLength={8} value={passwords.new_password} onChange={(e) => setPasswords({ ...passwords, new_password: e.target.value })} /></label>
          <button className="btn btn-primary w-fit" type="submit">Change Password</button>
        </form>
      </section>
    </div>
  );
}
