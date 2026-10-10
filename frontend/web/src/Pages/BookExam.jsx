import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Loader from "../components/common/loader";
import { getStored, getProfile, getUserId, getBookName } from "../utils/lesson";

export default function BookExam() {
  const navigate = useNavigate();
  const profile = getProfile();
  const book = getStored("current_book");

  const [exam, setExam] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [answers, setAnswers] = useState({});
  const [index, setIndex] = useState(0);
  const [result, setResult] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [attempt, setAttempt] = useState(0);

  // Called from buttons, not from the effect, so setting state here is fine.
  const retry = () => {
    setLoading(true);
    setError("");
    setResult(null);
    setExam(null);
    setAnswers({});
    setIndex(0);
    setAttempt((n) => n + 1);
  };

  useEffect(() => {
    if (!profile || !book?.file_name) {
      navigate("/library");
      return;
    }

    let cancelled = false;

    api
      .post(
        "/book/exam",
        {
          book: book.file_name,
          user_id: getUserId(),
          language: profile.learning_language,
          target_language: profile.native_language,
          learner_level: profile.learner_level,
        },
        { timeout: 180000 },
      )
      .then((response) => {
        if (!cancelled) setExam(response.data);
      })
      .catch((err) => {
        if (!cancelled) {
          setError(
            err?.response?.data?.error ||
              "Couldn't prepare the exam. Please try again.",
          );
        }
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [attempt]);

  const submit = async () => {
    const unanswered = exam.questions.filter(
      (q) => !String(answers[q.id] || "").trim(),
    ).length;

    if (
      unanswered &&
      !window.confirm(`${unanswered} question(s) are empty. Submit anyway?`)
    )
      return;

    try {
      setSubmitting(true);
      const response = await api.post("/book/exam/submit", {
        exam_id: exam.exam_id,
        user_id: getUserId(),
        book_name: getBookName(book),
        answers,
      });
      setResult(response.data);
    } catch (err) {
      setError(err?.response?.data?.error || "Couldn't submit the exam.");
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <Loader label="Preparing your final exam..." />;

  if (error && !exam) {
    return (
      <div className="exam-page">
        <h1>🎓 Final Book Exam</h1>
        <p className="exam-error">{error}</p>
        <div className="exam-nav">
          <button onClick={() => navigate("/lesson")}>← Back to lesson</button>
          <button className="exam-primary" onClick={retry}>
            Try again
          </button>
        </div>
      </div>
    );
  }

  if (!exam) return null;

  if (result) {
    return (
      <div className="exam-page">
        <h1>{result.passed ? "🎉 You passed!" : "Keep practicing"}</h1>

        <div className="exam-score">
          <h2>{result.percent}%</h2>
          <p>
            {result.score} of {result.total} correct • pass mark{" "}
            {result.pass_percent}%
          </p>
          {result.xp_awarded > 0 && <p>+{result.xp_awarded} XP earned</p>}
        </div>

        {result.results.map((r, i) => (
          <div
            key={r.id}
            className={`exam-result-row ${r.correct ? "correct" : "wrong"}`}
          >
            <strong>
              {i + 1}. {r.question}
            </strong>
            <p>Your answer: {r.your_answer || "—"}</p>
            {!r.correct && <p>Correct answer: {r.correct_answer}</p>}
            {r.explanation && <small>{r.explanation}</small>}
          </div>
        ))}

        <div className="exam-nav">
          <button onClick={() => navigate("/library")}>Back to library</button>
          <button className="exam-primary" onClick={retry}>
            Retake with new questions
          </button>
        </div>
      </div>
    );
  }

  const question = exam.questions[index];
  const isLast = index === exam.questions.length - 1;

  return (
    <div className="exam-page">
      <h1>🎓 {exam.title}</h1>
      <p className="exam-progress">
        Question {index + 1} of {exam.questions.length}
      </p>

      <div className="exam-card">
        <h3>{question.question}</h3>

        {question.type === "multiple_choice" ? (
          <div className="exam-options">
            {question.options.map((option) => (
              <button
                key={option}
                className={`exam-option ${answers[question.id] === option ? "selected" : ""}`}
                onClick={() =>
                  setAnswers({ ...answers, [question.id]: option })
                }
              >
                {option}
              </button>
            ))}
          </div>
        ) : (
          <textarea
            className="exam-input"
            rows={3}
            placeholder="Type your translation..."
            value={answers[question.id] || ""}
            onChange={(e) =>
              setAnswers({ ...answers, [question.id]: e.target.value })
            }
          />
        )}
      </div>

      {error && <p className="exam-error">{error}</p>}

      <div className="exam-nav">
        <button onClick={() => setIndex(index - 1)} disabled={index === 0}>
          ← Previous
        </button>

        {isLast ? (
          <button
            className="exam-primary"
            onClick={submit}
            disabled={submitting}
          >
            {submitting ? "Grading..." : "Submit exam"}
          </button>
        ) : (
          <button className="exam-primary" onClick={() => setIndex(index + 1)}>
            Next →
          </button>
        )}
      </div>
    </div>
  );
}
