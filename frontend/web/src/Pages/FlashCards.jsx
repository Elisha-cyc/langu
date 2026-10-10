import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Loader from "../components/common/loader";
import { getProfile, getUserId, audioUrl } from "../utils/lesson";

export default function Flashcards() {
  const navigate = useNavigate();
  const profile = getProfile();
  const userId = getUserId();
  const language = profile?.learning_language;

  const [tab, setTab] = useState("review");
  const [cards, setCards] = useState([]);
  const [words, setWords] = useState([]);
  const [dueTotal, setDueTotal] = useState(0);
  const [revealed, setRevealed] = useState(false);
  const [loading, setLoading] = useState(true);
  const [reviewed, setReviewed] = useState(0);
  const [xp, setXp] = useState(0);

  useEffect(() => {
    if (!profile) {
      navigate("/");
      return;
    }

    let cancelled = false;

    Promise.all([
      api.get("/vocab/due", { params: { user_id: userId, language } }),
      api.get("/vocab/list", { params: { user_id: userId, language } }),
    ])
      .then(([due, all]) => {
        if (cancelled) return;
        setCards(due.data.cards || []);
        setDueTotal(due.data.due_total || 0);
        setWords(all.data.words || []);
      })
      .catch((error) => console.error(error))
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const card = cards[0];

  const speak = async () => {
    if (!card) return;
    try {
      const res = await api.post("/audio/read", {
        text: card.word.split("(")[0].trim(),
        language,
      });
      new Audio(audioUrl(res.data.audio)).play();
    } catch (error) {
      console.warn("No voice for this word:", error);
    }
  };

  const grade = async (quality) => {
    try {
      const res = await api.post("/vocab/review", {
        user_id: userId,
        card_id: card.id,
        quality,
      });
      setXp((x) => x + (res.data.xp_awarded || 0));
    } catch (error) {
      console.error(error);
    }
    // "Again" puts the card at the back of today's pile
    setCards((prev) =>
      quality < 3 ? [...prev.slice(1), prev[0]] : prev.slice(1),
    );
    setReviewed((n) => n + 1);
    setRevealed(false);
  };

  const remove = async (id) => {
    await api.delete(`/vocab/${id}`, { params: { user_id: userId } });
    setWords((prev) => prev.filter((w) => w.id !== id));
    setCards((prev) => prev.filter((c) => c.id !== id));
  };

  if (loading) return <Loader label="Loading your flashcards..." />;

  return (
    <div className="flash-page">
      <div className="flash-header">
        <button className="back-btn" onClick={() => navigate("/home")}>
          ←
        </button>
        <div>
          <h1>🧠 Flashcards</h1>
          <p>
            {language} • {words.length} saved words
          </p>
        </div>
      </div>

      <div className="library-tabs">
        <button
          className={tab === "review" ? "active-tab" : ""}
          onClick={() => setTab("review")}
        >
          Review ({dueTotal})
        </button>
        <button
          className={tab === "words" ? "active-tab" : ""}
          onClick={() => setTab("words")}
        >
          All words
        </button>
      </div>

      {tab === "review" && (
        <>
          {!card ? (
            <div className="empty-library">
              <h3>
                {words.length === 0
                  ? "No saved words yet"
                  : "All done for today 🎉"}
              </h3>
              <p>
                {words.length === 0
                  ? "Open a lesson and tap “＋ Save” next to a vocabulary word."
                  : `You reviewed ${reviewed} card(s) and earned ${xp} XP. Come back tomorrow.`}
              </p>
              <button
                className="exam-primary"
                onClick={() => navigate("/library")}
              >
                Open library
              </button>
            </div>
          ) : (
            <div className="flash-card">
              <p className="flash-count">{cards.length} left today</p>
              <h2>{card.word}</h2>
              <button
                className="speaker-btn"
                onClick={speak}
                aria-label="Hear the word"
              >
                🔊
              </button>

              {revealed ? (
                <>
                  <p className="flash-meaning">
                    {card.meaning || "No meaning saved."}
                  </p>
                  <div className="flash-actions">
                    <button onClick={() => grade(1)}>
                      Again<small>tomorrow</small>
                    </button>
                    <button onClick={() => grade(4)}>
                      Good<small>later</small>
                    </button>
                    <button onClick={() => grade(5)}>
                      Easy<small>much later</small>
                    </button>
                  </div>
                </>
              ) : (
                <button
                  className="exam-primary"
                  onClick={() => setRevealed(true)}
                >
                  Show meaning
                </button>
              )}
            </div>
          )}
        </>
      )}

      {tab === "words" && (
        <div className="flash-list">
          {words.length === 0 && (
            <p className="library-note">Nothing saved yet.</p>
          )}
          {words.map((w) => (
            <div key={w.id} className="flash-list-row">
              <div>
                <strong>{w.word}</strong>
                <span>{w.meaning}</span>
              </div>
              <button
                onClick={() => remove(w.id)}
                aria-label={`Delete ${w.word}`}
              >
                🗑
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
