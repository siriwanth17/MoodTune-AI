import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { LogIn } from "lucide-react";
import AuthForm from "../components/AuthForm";
import { useAuth } from "../contexts/AuthContext";
import { apiMessage } from "../api/client";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState("");
  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      await login(form);
      navigate("/");
    } catch (err) {
      setError(apiMessage(err));
    }
  }
  return (
    <AuthForm title="Welcome back" subtitle="Sign in to continue your emotion-aware listening session." footer={<><Link className="font-bold text-[#176b87]" to="/forgot-password">Forgot password?</Link> · <Link className="font-bold text-[#176b87]" to="/register">Create account</Link></>}>
      <form className="grid gap-4" onSubmit={submit}>
        {error && <p className="rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</p>}
        <label className="grid gap-1"><span className="label">Email</span><input className="input" type="email" required value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} /></label>
        <label className="grid gap-1"><span className="label">Password</span><input className="input" type="password" required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label>
        <button className="btn btn-primary" type="submit"><LogIn size={18} /> Login</button>
      </form>
    </AuthForm>
  );
}
