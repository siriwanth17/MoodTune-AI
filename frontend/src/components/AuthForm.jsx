import { Link } from "react-router-dom";
import { Music2 } from "lucide-react";

export default function AuthForm({ title, subtitle, children, footer }) {
  return (
    <main className="screen-center px-4">
      <section className="panel w-full max-w-md p-6">
        <Link to="/" className="mb-5 flex items-center gap-2 text-2xl font-black text-[#174454]"><Music2 /> MoodTune AI</Link>
        <h1 className="text-2xl font-black">{title}</h1>
        <p className="mt-1 text-sm text-slate-600">{subtitle}</p>
        <div className="mt-6">{children}</div>
        {footer && <div className="mt-5 text-sm text-slate-600">{footer}</div>}
      </section>
    </main>
  );
}
