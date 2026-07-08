import { useState } from "react";
import { Link } from "react-router-dom";
import AuthForm from "../components/AuthForm";
import { api, apiMessage } from "../api/client";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");
  async function submit(event) {
    event.preventDefault();
    try {
      const { data } = await api.post("/auth/forgot-password", { email });
      setMessage(data.reset_token ? `Reset token: ${data.reset_token}` : data.message);
    } catch (err) {
      setMessage(apiMessage(err));
    }
  }
  return (
    <AuthForm title="Reset access" subtitle="Generate a secure password reset token for your account." footer={<Link className="font-bold text-[#176b87]" to="/login">Back to login</Link>}>
      <form className="grid gap-4" onSubmit={submit}>
        {message && <p className="rounded-md bg-emerald-50 p-3 text-sm text-emerald-800 break-words">{message}</p>}
        <label className="grid gap-1"><span className="label">Email</span><input className="input" type="email" required value={email} onChange={(e) => setEmail(e.target.value)} /></label>
        <button className="btn btn-primary" type="submit">Send Reset Token</button>
      </form>
    </AuthForm>
  );
}
