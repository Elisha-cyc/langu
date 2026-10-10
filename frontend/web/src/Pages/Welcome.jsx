// frontend/web/src/Pages/Welcome.jsx
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

// All 20 languages (the old list had only 7).
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
// Only the 3 levels the curriculum has ("Elementary" had no lessons).
const LEVELS = ["Beginner", "Intermediate", "Advanced"];

export default function Welcome() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [nativeLanguage, setNativeLanguage] = useState("English");
  const [learningLanguage, setLearningLanguage] = useState("Japanese");
  const [level, setLevel] = useState("Beginner");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (localStorage.getItem("lingua_profile")) navigate("/home");
  }, [navigate]);

  const handleStart = async () => {
    if (!name.trim()) {
      alert("Please enter your name.");
      return;
    }

    if (nativeLanguage === learningLanguage) {
      alert("Choose two different languages.");
      return;
    }

    setLoading(true);

    try {
      const response = await api.post("/profile", {
        name: name.trim(),
        native_language: nativeLanguage,
        learning_language: learningLanguage,
        learner_level: level,
      });

      const userId = response.data.user_id;

      // Saved as both "id" and "user_id": different pages read different names.
      const fullProfile = {
        id: userId,
        user_id: userId,
        name: name.trim(),
        native_language: nativeLanguage,
        learning_language: learningLanguage,
        learner_level: level,
      };

      localStorage.setItem("lingua_profile", JSON.stringify(fullProfile));
      localStorage.setItem("lingua_user", userId);

      navigate("/home");
    } catch (error) {
      console.error(error);
      alert(error?.response?.data?.error || "Unable to create profile.");
    } finally {
      setLoading(false);
    }
  };

  const hasTwi = nativeLanguage === "Twi" || learningLanguage === "Twi";

  return (
    <div className="welcome-page">
      <div className="welcome-card">
        <h1>Lingua AI</h1>
        <p>Your personal AI language teacher</p>

        <label>Your Name</label>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter your name"
        />

        <label>Native Language</label>
        <select
          value={nativeLanguage}
          onChange={(e) => setNativeLanguage(e.target.value)}
        >
          {NATIVE.map((l) => (
            <option key={l}>{l}</option>
          ))}
        </select>

        <label>Language to Learn</label>
        <select
          value={learningLanguage}
          onChange={(e) => setLearningLanguage(e.target.value)}
        >
          {LEARN.map((l) => (
            <option key={l}>{l}</option>
          ))}
        </select>

        <label>Difficulty</label>
        <select value={level} onChange={(e) => setLevel(e.target.value)}>
          {LEVELS.map((l) => (
            <option key={l}>{l}</option>
          ))}
        </select>

        {hasTwi && (
          <p className="notice-banner" style={{ marginTop: 16 }}>
            The AI cannot teach or explain in Twi yet. Twi lessons use the
            built-in curriculum and explanations are given in English.
          </p>
        )}

        <button onClick={handleStart} disabled={loading}>
          {loading ? "Creating Profile..." : "Start Learning"}
        </button>
      </div>
    </div>
  );
}
