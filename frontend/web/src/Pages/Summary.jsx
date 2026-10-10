// frontend/web/src/Pages/Summary.jsx
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Loader from "../components/common/loader";
import { getProfile, getStored, audioUrl } from "../utils/lesson";

export default function Summary() {
  const navigate = useNavigate();
  const profile = getProfile();

  const [summary, setSummary] = useState("");
  const [language, setLanguage] = useState(profile?.native_language);
  const [playing, setPlaying] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const audioRef = useRef(null);

  const lesson = getStored("generated_lesson");

  const read = async (text, lang) => {
    if (!text) return;
    if (audioRef.current) audioRef.current.pause();

    try {
      const response = await api.post("/audio/read", { text, language: lang });
      const player = new Audio(audioUrl(response.data.audio));
      audioRef.current = player;
      player.onended = () => setPlaying(false);
      await player.play();
      setPlaying(true);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    const load = async () => {
      const scanText = localStorage.getItem("scan_text");

      if (!profile || !lesson || !scanText) {
        navigate("/study-mode");
        return;
      }

      try {
        // A real AI summary of the scanned text. The old page only showed the
        // translation of the sentences and called it a summary.
        const response = await api.post(
          "/text/summarize",
          {
            text: scanText,
            mode: "summary",
            language: profile.learning_language,
            target_language: profile.native_language,
            learner_level: profile.learner_level,
          },
          { timeout: 120000 },
        );

        const spokenIn = response.data.explained_in || profile.native_language;
        setSummary(response.data.result);
        setLanguage(spokenIn);
        read(response.data.result, spokenIn);
      } catch (err) {
        setError(err?.response?.data?.error || "Couldn't write the summary.");
      } finally {
        setLoading(false);
      }
    };

    load();
    return () => {
      if (audioRef.current) audioRef.current.pause();
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const pause = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      setPlaying(false);
    }
  };

  if (loading) return <Loader label="Writing your summary..." />;

  return (
    <div className="summary-page">
      <div className="summary-header">
        <button className="back-btn" onClick={() => navigate("/study-mode")}>
          ←
        </button>
        <div>
          <h1>📖 Summary</h1>
          <p>{lesson?.title}</p>
        </div>
      </div>

      <div className="teacher-banner">
        <h3>🔊 AI Teacher</h3>
        <p>{playing ? "Reading the summary..." : "Summary ready."}</p>
        <div className="teacher-buttons">
          <button onClick={() => read(summary, language)}>▶ Replay</button>
          <button onClick={pause}>⏸ Pause</button>
        </div>
      </div>

      <div className="summary-card">
        <h2>Easy Explanation</h2>
        <p>{error || summary}</p>
      </div>
    </div>
  );
}
