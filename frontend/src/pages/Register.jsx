import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { UserPlus } from "lucide-react";
import AuthForm from "../components/AuthForm";
import { useAuth } from "../contexts/AuthContext";
import { apiMessage } from "../api/client";

export default function Register() {
  const { register } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "", favourite_genres: "pop, acoustic" });
  const [error, setError] = useState("");
  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      await register({ ...form, favourite_genres: form.favourite_genres.split(",").map((x) => x.trim()).filter(Boolean) });
      navigate("/");
    } catch (err) {
      setError(apiMessage(err));
    }
  }
  return (
    <AuthForm title="Create your account" subtitle="The first registered account becomes the admin for this deployment." footer={<Link className="font-bold text-[#176b87]" to="/login">Already have an account?</Link>}>
      <form className="grid gap-4" onSubmit={submit}>
        {error && <p className="rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        <label className="grid gap-1"><span className="label">Name</span><input className="input" required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} /></label>
        <label className="grid gap-1"><span className="label">Email</span><input className="input" type="email" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>
        <label className="grid gap-1"><span className="label">Password</span><input className="input" type="password" minLength={8} required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label>
        <label className="grid gap-1"><span className="label">Favourite genres</span><input className="input" value={form.favourite_genres} onChange={(e) => setForm({ ...form, favourite_genres: e.target.value })} /></label>
        <button className="btn btn-primary" type="submit"><UserPlus size={18} /> Register</button>
      </form>
    </AuthForm>
  );
}
