// frontend/web/src/Pages/Profile.jsx   (was an empty stub)
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Loader from "../components/common/loader";
import { getProfile, getUserId } from "../utils/lesson";

const LEARN = [
  "Arabic",
  "Chinese",
  "Dutch",
  "French",
  "German",
  "Greek",
  "Hebrew",
  "Hindi",
  "Italian",
  "Japanese",
  "Korean",
  "Polish",
  "Portuguese",
  "Russian",
  "Spanish",
  "Swedish",
  "Thai",
  "Turkish",
  "Twi",
  "Vietnamese",
];
const NATIVE = ["English", ...LEARN];
const LEVELS = ["Beginner", "Intermediate", "Advanced"];

export default function Profile() {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [form, setForm] = useState(null);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    const load = async () => {
      try {
        const res = await api.get(`/dashboard?user_id=${getUserId()}`);
        setData(res.data);
        setForm({
          native_language: res.data.user.native_language,
          learning_language: res.data.user.learning_language,
          learner_level: res.data.user.learner_level,
        });
      } catch (error) {
        console.error(error);
      }
    };
    load();
  }, []);

  const save = async () => {
    if (form.native_language === form.learning_language) {
      setMessage("Choose two different languages.");
      return;
    }

    try {
      setSaving(true);
      const res = await api.put(`/profile/${getUserId()}`, form);

      // Same user, new settings (the old flow created a brand new user)
      const stored = { ...getProfile(), ...res.data, user_id: getUserId() };
      localStorage.setItem("lingua_profile", JSON.stringify(stored));
      localStorage.removeItem("current_book");
      setMessage("Saved. Your library now matches your new settings.");
    } catch (error) {
      setMessage(error?.response?.data?.error || "Couldn't save your changes.");
    } finally {
      setSaving(false);
    }
  };

  const logout = () => {
    if (
      !window.confirm(
        "Log out on this device? Your progress stays saved on the server.",
      )
    )
      return;
    Object.keys(localStorage)
      .filter(
        (k) =>
          k.startsWith("lingua_") ||
          [
            "current_book",
            "generated_lesson",
            "scan_text",
            "scan_audio",
            "study_source",
            "sleep_progress",
          ].includes(k),
      )
      .forEach((k) => localStorage.removeItem(k));
    navigate("/");
  };

  if (!data || !form) return <Loader label="Loading your profile..." />;

  const { user, progress, streak, words_saved: wordsSaved } = data;
  const levelProgress = user.xp % 100;

  return (
    <div className="profile-page">
      <div className="flash-header">
        <button className="back-btn" onClick={() => navigate("/home")}>
          ←
        </button>
        <div>
          <h1>{user.name}</h1>
          <p>
            Level {user.level} • {user.xp} XP
          </p>
        </div>
      </div>

      <div className="progress-track profile-xp">
        <div className="progress-fill" style={{ width: `${levelProgress}%` }} />
      </div>
      <p className="library-note">
        {100 - levelProgress} XP to level {user.level + 1}
      </p>

      <div className="stats-grid">
        <div className="stat-card">
          <h2>🔥 {streak}</h2>
          <p>Day streak</p>
        </div>
        <div className="stat-card">
          <h2>{progress.accuracy}%</h2>
          <p>Speaking accuracy</p>
        </div>
        <div className="stat-card">
          <h2>{progress.lessons_completed}</h2>
          <p>Pages mastered</p>
        </div>
        <div className="stat-card">
          <h2>{wordsSaved}</h2>
          <p>Saved words</p>
        </div>
      </div>

      <div className="profile-card">
        <h3>Language settings</h3>

        <label>I speak</label>
        <select
          value={form.native_language}
          onChange={(e) =>
            setForm({ ...form, native_language: e.target.value })
          }
        >
          {NATIVE.map((l) => (
            <option key={l}>{l}</option>
          ))}
        </select>

        <label>I want to learn</label>
        <select
          value={form.learning_language}
          onChange={(e) =>
            setForm({ ...form, learning_language: e.target.value })
          }
        >
          {LEARN.map((l) => (
            <option key={l}>{l}</option>
          ))}
        </select>

        <label>Level</label>
        <select
          value={form.learner_level}
          onChange={(e) => setForm({ ...form, learner_level: e.target.value })}
        >
          {LEVELS.map((l) => (
            <option key={l}>{l}</option>
          ))}
        </select>

        {(form.native_language === "Twi" ||
          form.learning_language === "Twi") && (
          <p className="notice-banner">
            The AI cannot explain in Twi or write Twi lessons yet. Twi lessons
            use the built-in curriculum, and explanations are given in English.
          </p>
        )}

        {message && <p className="library-note">{message}</p>}

        <button className="exam-primary" onClick={save} disabled={saving}>
          {saving ? "Saving..." : "Save changes"}
        </button>
        <button className="logout-btn" onClick={logout}>
          Log out
        </button>
      </div>
    </div>
  );
}
