import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Loader from "../components/common/loader";
import { getUserId } from "../utils/lesson";

export default function Home() {
  const navigate = useNavigate();
  const [dashboard, setDashboard] = useState(null);
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);

  // Called from a button, not from the effect.
  const retry = () => {
    setError("");
    setDashboard(null);
    setAttempt((n) => n + 1);
  };

  useEffect(() => {
    let cancelled = false;

    api
      .get(`/dashboard?user_id=${getUserId()}`)
      .then((response) => {
        if (!cancelled) setDashboard(response.data);
      })
      .catch((err) => {
        console.error(err);
        if (!cancelled) {
          setError(
            err?.response?.data?.error || "Couldn't load your dashboard.",
          );
        }
      });

    return () => {
      cancelled = true;
    };
  }, [attempt]);

  if (error) {
    return (
      <div className="home-page">
        <p className="library-note error">{error}</p>
        <button className="continue-btn" onClick={retry}>
          Try again
        </button>
      </div>
    );
  }

  if (!dashboard) return <Loader label="Loading dashboard..." />;

  return (
    <div className="home-page">
      <div className="hero">
        <h1>Welcome back, {dashboard.user.name}</h1>
        <p>
          {dashboard.user.native_language}
          {" → "}
          {dashboard.user.learning_language}
        </p>
        <p>Level: {dashboard.user.learner_level}</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h2>{dashboard.user.xp}</h2>
          <p>XP • Level {dashboard.user.level}</p>
        </div>
        <div className="stat-card">
          <h2>🔥 {dashboard.streak}</h2>
          <p>Day streak</p>
        </div>
        <div className="stat-card">
          <h2>{dashboard.progress.lessons_completed}</h2>
          <p>Pages mastered</p>
        </div>
        <div className="stat-card">
          <h2>{dashboard.progress.accuracy}%</h2>
          <p>Speaking accuracy</p>
        </div>
      </div>

      <div className="home-actions">
        <button className="continue-btn" onClick={() => navigate("/library")}>
          Open Library
        </button>

        <button
          className="continue-btn"
          onClick={() => navigate("/flashcards")}
        >
          🧠 Review flashcards
          {dashboard.due_cards > 0 ? ` (${dashboard.due_cards} due)` : ""}
        </button>

        <button className="continue-btn" onClick={() => navigate("/scan")}>
          📷 Scan a page
        </button>

        <button className="sleep-btn" onClick={() => navigate("/sleep-mode")}>
          <span className="sleep-btn-icon">🌙</span>
          <span className="sleep-btn-text">
            <strong>Sleep Teacher</strong>
            <small>Learn while you drift off</small>
          </span>
          <span className="sleep-btn-arrow">→</span>
        </button>

        <button className="continue-btn" onClick={() => navigate("/profile")}>
          👤 Profile & settings
        </button>
      </div>
    </div>
  );
}
