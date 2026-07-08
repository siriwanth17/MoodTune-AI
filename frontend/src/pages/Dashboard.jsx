import { useEffect, useRef, useState } from "react";
import Webcam from "react-webcam";
import { motion } from "framer-motion";
import { Camera, Heart, PlayCircle, RefreshCw } from "lucide-react";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api, apiMessage } from "../api/client";
import { useAuth } from "../contexts/AuthContext";

const chartSeed = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((day, i) => ({ day, happy: 2 + i, sad: i % 3, neutral: 4 - (i % 2) }));

export default function Dashboard() {
  const { user } = useAuth();
  const webcam = useRef(null);
  const [camera, setCamera] = useState("Camera Connected");
  const [emotion, setEmotion] = useState(null);
  const [recommendation, setRecommendation] = useState(null);
  const [history, setHistory] = useState([]);
  const [favorites, setFavorites] = useState([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    const [rec, fav] = await Promise.all([api.get("/recommendations/history"), api.get("/favorites")]);
    setHistory(rec.data);
    setFavorites(fav.data);
  }

  useEffect(() => { load().catch(() => {}); }, []);

  async function detect() {
    const image = webcam.current?.getScreenshot();
    if (!image) {
      setCamera("Camera Permission Error");
      return;
    }
    setBusy(true);
    setError("");
    try {
      const { data } = await api.post("/emotions/detect", { image });
      setEmotion(data);
      setCamera(data.camera_status);
      const rec = await api.post("/recommendations", { emotion: data.emotion, confidence: data.confidence });
      setRecommendation(rec.data);
      await load();
    } catch (err) {
      setError(apiMessage(err));
      const status = err?.response?.data?.detail?.camera_status;
      if (status) setCamera(status);
    } finally {
      setBusy(false);
    }
  }

  async function favorite(track) {
    await api.post("/favorites", { track });
    await load();
  }

  const tracks = recommendation?.tracks || history[0]?.tracks || [];
  return (
    <div className="grid gap-6">
      <section className="panel p-5">
        <h1 className="text-2xl font-black">Welcome, {user?.name}</h1>
        <p className="text-slate-600">Detect your expression and get a listening queue shaped by mood, favorites, history, and time of day.</p>
      </section>

      <div className="grid gap-6 lg:grid-cols-[380px_1fr]">
        <section className="panel p-4">
          <div className="mb-3 flex items-center justify-between"><h2 className="font-black">Emotion Detection</h2><span className="rounded bg-slate-100 px-2 py-1 text-xs font-bold">{camera}</span></div>
          <Webcam ref={webcam} audio={false} mirrored screenshotFormat="image/jpeg" videoConstraints={{ facingMode: "user" }} onUserMedia={() => setCamera("Camera Connected")} onUserMediaError={() => setCamera("Camera Permission Error")} className="aspect-video w-full rounded-md bg-slate-900 object-cover" />
          {error && <p className="mt-3 rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</p>}
          <button className="btn btn-primary mt-4 w-full" onClick={detect} disabled={busy}>{busy ? <RefreshCw className="animate-spin" size={18} /> : <Camera size={18} />} Detect Mood</button>
          {emotion && <div className="mt-4 grid grid-cols-3 gap-2 text-sm"><div className="stat"><b>{emotion.emotion}</b><span>Emotion</span></div><div className="stat"><b>{emotion.confidence}%</b><span>Confidence</span></div><div className="stat"><b>{emotion.processing_time_ms}ms</b><span>Time</span></div></div>}
        </section>

        <section className="panel p-4">
          <h2 className="mb-3 font-black">Music Recommendations</h2>
          <div className="track-grid">
            {tracks.map((track) => (
              <motion.article className="track-card" key={track.track_id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
                <img src={track.album_cover || "https://images.unsplash.com/photo-1511379938547-c1f69419868d?w=600"} alt="" />
                <div className="grid gap-2 p-3">
                  <div><h3 className="font-black">{track.title}</h3><p className="text-sm text-slate-600">{track.artist}</p></div>
                  <div className="flex items-center justify-between gap-2">
                    <span className="rounded bg-slate-100 px-2 py-1 text-xs font-bold">{track.genre} · {track.source}</span>
                    <div className="flex gap-1">
                      {track.spotify_url && <a className="btn btn-secondary p-2" href={track.spotify_url} target="_blank" rel="noreferrer"><PlayCircle size={16} /></a>}
                      <button className="btn btn-secondary p-2" onClick={() => favorite(track)}><Heart size={16} /></button>
                    </div>
                  </div>
                </div>
              </motion.article>
            ))}
          </div>
        </section>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        <section className="panel p-4 lg:col-span-2"><h2 className="mb-3 font-black">Weekly Mood Chart</h2><ResponsiveContainer height={260}><AreaChart data={chartSeed}><CartesianGrid strokeDasharray="3 3" /><XAxis dataKey="day" /><YAxis /><Tooltip /><Area dataKey="happy" stroke="#176b87" fill="#c8edf3" /><Area dataKey="neutral" stroke="#6b7280" fill="#e5e7eb" /></AreaChart></ResponsiveContainer></section>
        <section className="panel p-4"><h2 className="mb-3 font-black">Favourite Songs</h2><div className="grid gap-2">{favorites.slice(0, 6).map((fav) => <p key={fav.id} className="rounded bg-slate-50 p-2 text-sm font-bold">{fav.track.title}<br /><span className="font-normal text-slate-500">{fav.track.artist}</span></p>)}</div></section>
      </div>

      <section className="panel p-4"><h2 className="mb-3 font-black">Recommendation History</h2><div className="grid gap-2">{history.map((item) => <p key={item.id} className="rounded bg-slate-50 p-3 text-sm"><b>{item.emotion}</b> · {item.source} · {new Date(item.created_at).toLocaleString()} · {item.tracks?.length || 0} tracks</p>)}</div></section>
    </div>
  );
}
