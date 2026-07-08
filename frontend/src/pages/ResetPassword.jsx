import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import AuthForm from "../components/AuthForm";
import { api, apiMessage } from "../api/client";

export default function ResetPassword() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ token: "", password: "" });
  const [message, setMessage] = useState("");
  async function submit(event) {
    event.preventDefault();
    try {
      await api.post("/auth/reset-password", form);
      navigate("/login");
    } catch (err) {
      setMessage(apiMessage(err));
    }
  }
  return (
    <AuthForm title="Set a new password" subtitle="Paste your reset token and choose a new password." footer={<Link className="font-bold text-[#176b87]" to="/login">Back to login</Link>}>
      <form className="grid gap-4" onSubmit={submit}>
        {message && <p className="rounded-md bg-red-50 p-3 text-sm text-red-700">{message}</p>}
        <label className="grid gap-1"><span className="label">Reset token</span><input className="input" required value={form.token} onChange={(e) => setForm({ ...form, token: e.target.value })} /></label>
        <label className="grid gap-1"><span className="label">New password</span><input className="input" type="password" minLength={8} required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} /></label>
        <button className="btn btn-primary" type="submit">Reset Password</button>
      </form>
    </AuthForm>
  );
}
