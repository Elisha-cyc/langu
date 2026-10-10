import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getStored, audioUrl } from "../utils/lesson";

export default function StudyMode() {
  const navigate = useNavigate();

  const [lesson] = useState(() => getStored("generated_lesson"));
  const [audioPlaying, setAudioPlaying] = useState(false);
  const audioRef = useRef(null);

  const pause = () => {
    if (audioRef.current) audioRef.current.pause();
  };

  const play = () => {
    const scanAudio = localStorage.getItem("scan_audio");
    if (!scanAudio || scanAudio === "null") return;

    pause();

    const player = new Audio(audioUrl(scanAudio));
    audioRef.current = player;
    player.onplaying = () => setAudioPlaying(true);
    player.onpause = () => setAudioPlaying(false);
    player.onended = () => setAudioPlaying(false);
    player.play().catch(() => setAudioPlaying(false));
  };

  useEffect(() => {
    if (!lesson) {
      navigate("/scan");
      return;
    }

    play();

    // Audio kept playing after leaving the page.
    return pause;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  if (!lesson) return null;

  return (
    <div className="study-mode-page">
      <div className="study-header">
        <button className="back-btn" onClick={() => navigate("/scan")}>
          ←
        </button>
        <h1>Choose How to Study</h1>
      </div>

      <div className="reading-status">
        <h3>🔊 AI Teacher</h3>
        <p>
          {audioPlaying ? "Reading the scanned page..." : "The page is ready."}
        </p>

        <div className="reading-buttons">
          <button onClick={play}>▶ Replay</button>
          <button onClick={pause}>⏸ Pause</button>
        </div>
      </div>

      <button
        className="study-card key"
        onClick={() => navigate("/key-factors")}
      >
        <h2>📌 Key Factors</h2>
        <p>
          Learn the important vocabulary, grammar and key ideas from this page.
        </p>
      </button>

      <button
        className="study-card summary"
        onClick={() => navigate("/summary")}
      >
        <h2>📖 Summary</h2>
        <p>Listen to an easy explanation in your native language.</p>
      </button>

      <button className="study-card lesson" onClick={() => navigate("/lesson")}>
        <h2>📘 Full Lesson</h2>
        <p>Interactive lesson with speaking, vocabulary, grammar and test.</p>
      </button>
    </div>
  );
}
