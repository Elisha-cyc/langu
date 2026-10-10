// frontend/web/src/Pages/KeyFactors.jsx
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Loader from "../components/common/loader";
import { getProfile, getStored, getUserId, audioUrl } from "../utils/lesson";

const SECTIONS = [
  ["main_ideas", "💡 Main ideas"],
  ["topics", "🗂 Topics"],
  ["grammar_patterns", "📝 Grammar patterns"],
  ["cultural_notes", "🌏 Cultural notes"],
];

// Turns the structured answer into plain sentences for the voice.
function toSpeech(data) {
  if (typeof data === "string") return data;

  const parts = [];
  SECTIONS.forEach(([key, title]) => {
    const items = (data[key] || []).filter(Boolean);
    if (items.length)
      parts.push(`${title.replace(/^\S+\s/, "")}. ${items.join(". ")}`);
  });

  const words = (data.vocabulary || []).map((v) => `${v.word}, ${v.meaning}`);
  if (words.length) parts.push(`Vocabulary. ${words.join(". ")}`);

  return parts.join(". ");
}

export default function KeyFactors() {
  const navigate = useNavigate();
  const profile = getProfile();

  const [title, setTitle] = useState("");
  const [data, setData] = useState(null); // object (book) or string (scan)
  const [language, setLanguage] = useState(profile?.native_language);
  const [playing, setPlaying] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const audioRef = useRef(null);

  const read = async (content, lang) => {
    const text = toSpeech(content);
    if (!text) return;
    if (audioRef.current) audioRef.current.pause();

    try {
      // The old page always read in English, whatever the learner's language.
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

  // The old file called loadKeyFactors() directly in the component body, so it
  // ran on EVERY render and sent API requests in an endless loop. It now runs once.
  useEffect(() => {
    const load = async () => {
      try {
        if (!profile) {
          navigate("/");
          return;
        }

        const common = {
          language: profile.learning_language,
          target_language: profile.native_language,
          learner_level: profile.learner_level,
        };

        let content, spokenIn;

        if (localStorage.getItem("study_source") === "scan") {
          const lesson = getStored("generated_lesson");
          const response = await api.post(
            "/text/summarize",
            {
              ...common,
              text: localStorage.getItem("scan_text"),
              mode: "key_points",
            },
            { timeout: 120000 },
          );
          content = response.data.result;
          spokenIn = response.data.explained_in || profile.native_language;
          setTitle(lesson?.title || "Scanned page");
        } else {
          const book = getStored("current_book");
          if (!book?.file_name) {
            navigate("/library");
            return;
          }
          const response = await api.post(
            "/book/key-factors",
            { ...common, book: book.file_name, user_id: getUserId() },
            { timeout: 180000 },
          );
          content = response.data.key_factors;
          spokenIn = response.data.explained_in || profile.native_language;
          setTitle(book.title || response.data.title);
        }

        setData(content);
        setLanguage(spokenIn);
        read(content, spokenIn);
      } catch (err) {
        setError(
          err?.response?.data?.error || "Couldn't load the key factors.",
        );
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

  if (loading) return <Loader label="Loading key factors..." />;

  return (
    <div className="key-page">
      <div className="key-header">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ←
        </button>
        <div>
          <h1>📌 Key Factors</h1>
          <p>{title}</p>
        </div>
      </div>

      <div className="teacher-banner">
        <h3>🔊 AI Teacher</h3>
        <p>{playing ? "Reading the key factors..." : "Key factors ready."}</p>
        <div className="teacher-buttons">
          <button onClick={() => read(data, language)}>▶ Replay</button>
          <button onClick={pause}>⏸ Pause</button>
        </div>
      </div>

      {error && (
        <div className="key-section">
          <p>{error}</p>
        </div>
      )}

      {typeof data === "string" && (
        <div className="key-section">
          <h2>📖 This page</h2>
          <pre style={{ whiteSpace: "pre-wrap", fontFamily: "inherit" }}>
            {data}
          </pre>
        </div>
      )}

      {data && typeof data === "object" && (
        <>
          {SECTIONS.map(([key, heading]) =>
            (data[key] || []).length > 0 ? (
              <div className="key-section" key={key}>
                <h2>{heading}</h2>
                <ul className="key-list">
                  {data[key].map((item, i) => (
                    <li key={i}>{item}</li>
                  ))}
                </ul>
              </div>
            ) : null,
          )}

          {(data.vocabulary || []).length > 0 && (
            <div className="key-section">
              <h2>📚 Vocabulary</h2>
              <ul className="key-list">
                {data.vocabulary.map((v, i) => (
                  <li key={i}>
                    <strong>{v.word}</strong> — {v.meaning}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </div>
  );
}
