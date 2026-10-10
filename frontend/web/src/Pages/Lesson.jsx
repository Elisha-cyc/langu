// frontend/web/src/Pages/Lesson.jsx
import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";
import Loader from "../components/common/loader";
import { useTheme } from "../hooks/useTheme";
import {
  getStored,
  getProfile,
  getUserId,
  getBookName,
  audioUrl,
  speechText,
  scoringAvailable,
  normalizeSteps,
  buildStaticContent,
  fetchLessonPage,
} from "../utils/lesson";

const READING_LABELS = {
  sentence: "the phrase",
  translation: "the translation",
  vocabulary: "the vocabulary",
  grammar: "the grammar note",
  examples: "the examples",
  practice: "the practice question",
};

const PASS_SCORE = 80;

const PAUSE = {
  translation: 1500,
  vocabulary: 1200,
  grammar: 1500,
  example: 1000,
  practice: 2000,
};

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

export default function Lesson() {
  const navigate = useNavigate();
  const [theme, toggleTheme] = useTheme();

  const profile = getProfile();
  const userId = getUserId();
  const book = getStored("current_book");
  const isScan = localStorage.getItem("study_source") === "scan";
  const bookName = isScan ? null : getBookName(book);

  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [lesson, setLesson] = useState(null);
  const [steps, setSteps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [loadError, setLoadError] = useState("");
  const [audioLoading, setAudioLoading] = useState(false);
  const [currentSentence, setCurrentSentence] = useState(0);
  const [changingPage, setChangingPage] = useState(false);
  const [completedPages, setCompletedPages] = useState(0);
  const [bookCompleted, setBookCompleted] = useState(false);

  const [autoMode, setAutoMode] = useState(false);
  const [readingSpeed, setReadingSpeed] = useState(1);
  const [readingSection, setReadingSection] = useState(null);

  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [recordedBlob, setRecordedBlob] = useState(null);
  const [recordedURL, setRecordedURL] = useState("");
  const [speakingResult, setSpeakingResult] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [pageUnlocked, setPageUnlocked] = useState(false);
  const [xpGained, setXpGained] = useState(0);
  const [savedWords, setSavedWords] = useState(new Set());

  const audioRef = useRef(null);
  const resolveRef = useRef(null);
  // Every read-aloud run gets a number. Stopping bumps it, so a run that was
  // started earlier can tell it is old and quit.
  const readToken = useRef(0);
  const sentenceRefs = useRef([]);
  const speakingSectionRef = useRef(null);
  const recordedURLRef = useRef("");
  const recordStartRef = useRef(0);
  const recordDurationRef = useRef(0);
  const [scrollToSpeaking, setScrollToSpeaking] = useState(false);

  const sentences = steps.map((s) => s.sentence);
  const currentTeaching = steps[currentSentence]?.teaching || {};
  const explainLanguage = lesson?.explained_in || profile?.native_language;
  const canScore = scoringAvailable(lesson?.language);

  // ================= Recording =================

  const resetRecording = () => {
    if (recordedURLRef.current) {
      URL.revokeObjectURL(recordedURLRef.current);
      recordedURLRef.current = "";
    }
    setRecordedBlob(null);
    setRecordedURL("");
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });

      const mimeType = MediaRecorder.isTypeSupported("audio/webm;codecs=opus")
        ? "audio/webm;codecs=opus"
        : MediaRecorder.isTypeSupported("audio/mp4")
          ? "audio/mp4"
          : "";

      const recorder = new MediaRecorder(
        stream,
        mimeType ? { mimeType } : undefined,
      );
      const chunks = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) chunks.push(event.data);
      };

      recorder.onstop = () => {
        const blob = new Blob(chunks, { type: mimeType || "audio/webm" });
        if (recordedURLRef.current) URL.revokeObjectURL(recordedURLRef.current);
        const url = URL.createObjectURL(blob);
        recordedURLRef.current = url;
        setRecordedBlob(blob);
        setRecordedURL(url);
        stream.getTracks().forEach((track) => track.stop());
      };

      recorder.start();
      recordStartRef.current = Date.now();
      setMediaRecorder(recorder);
      setRecording(true);
    } catch (err) {
      console.error("getUserMedia failed:", err);
      alert("Microphone permission denied.");
    }
  };

  const stopRecording = () => {
    if (!mediaRecorder) return;
    recordDurationRef.current = Date.now() - recordStartRef.current;
    mediaRecorder.stop();
    setRecording(false);
  };

  const playRecording = () => {
    if (!recordedURL) return;
    new Audio(recordedURL)
      .play()
      .catch(() => alert("Couldn't play back the recording."));
  };

  // ================= Loading helpers =================

  const applyLesson = (data, startPage) => {
    setLesson(data);
    setPage(startPage);
    setTotalPages(data.total_pages || 1);
    setSteps(normalizeSteps(data.content));
    setCurrentSentence(0);
  };

  const loadPageStatus = async (currentPage) => {
    if (!bookName) {
      setPageUnlocked(false);
      return;
    }
    try {
      const response = await api.post("/page/status", {
        user_id: userId,
        book_name: bookName,
        page: currentPage,
      });
      setPageUnlocked(Boolean(response.data?.passed));
    } catch {
      setPageUnlocked(false);
    }
  };

  // total is passed in: reading totalPages from state gave 1 right after loading.
  const loadBookProgress = async (total) => {
    if (!bookName) return;
    try {
      const response = await api.post("/book/progress", {
        user_id: userId,
        book_name: bookName,
        total_pages: total,
      });
      setCompletedPages(response.data.completed_pages);
      setBookCompleted(response.data.book_completed);
    } catch (error) {
      console.warn("Book progress unavailable:", error);
    }
  };

  const loadLesson = async () => {
    try {
      if (!profile) {
        navigate("/");
        return;
      }

      const scanLesson = isScan ? getStored("generated_lesson") : null;

      if (scanLesson) {
        applyLesson(scanLesson, 1);
        return;
      }

      if (!book) {
        navigate("/library");
        return;
      }

      if (book.vocab) {
        applyLesson(
          {
            language: profile.learning_language,
            explained_in: "English",
            total_pages: 1,
            content: buildStaticContent(book),
          },
          1,
        );
        await loadPageStatus(1);
        await loadBookProgress(1);
        return;
      }

      let startPage = 1;

      if (book.file_name) {
        try {
          const resume = await api.get("/book/resume", {
            params: { user_id: userId, book_name: bookName },
          });
          startPage = resume.data.page || 1;
        } catch {
          startPage = 1;
        }
      }

      // Opens curriculum lessons, PDFs, DOCX and online books the same way.
      const data = await fetchLessonPage(book, startPage, profile);

      applyLesson(data, startPage);
      await loadPageStatus(startPage);
      await loadBookProgress(data.total_pages || 1);
    } catch (error) {
      console.error("Lesson error:", error);
      setLoadError(
        error?.response?.data?.error ||
          error?.message ||
          "Failed to load lesson.",
      );
    } finally {
      setLoading(false);
    }
  };

  // ================= Pronunciation =================

  const analyzePronunciation = async () => {
    if (!recordedBlob) return;

    if (recordDurationRef.current < 800 || recordedBlob.size < 2000) {
      alert("That recording was too short. Please record yourself speaking.");
      return;
    }

    try {
      setAnalyzing(true);

      const form = new FormData();
      form.append("audio", recordedBlob, "recording.webm");
      form.append("expected", sentences[currentSentence] || "");
      form.append("language", lesson.language);
      form.append("user_id", userId);
      form.append("page", page);
      if (bookName) form.append("book_name", bookName);

      const response = await api.post("/pronunciation/analyze", form, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 60000,
      });

      const data = response.data;
      setSpeakingResult(data);

      if (data.passed) {
        setPageUnlocked(true);
        if (data.xp_awarded) setXpGained(data.xp_awarded);
        await loadBookProgress(totalPages);
      }
    } catch (error) {
      console.error(error);
      alert(error?.response?.data?.error || "Pronunciation analysis failed.");
    } finally {
      setAnalyzing(false);
    }
  };

  // Languages without speaking scores (Twi): the learner confirms practice.
  const markPracticed = async () => {
    try {
      const response = await api.post("/page/complete", {
        user_id: userId,
        book_name: bookName,
        page,
        language: lesson.language,
      });
      setPageUnlocked(true);
      setXpGained(response.data.xp_awarded || 0);
      await loadBookProgress(totalPages);
    } catch (error) {
      alert(error?.response?.data?.error || "Couldn't save your progress.");
    }
  };

  // ================= Flashcards =================

  const saveWord = async (item) => {
    try {
      await api.post("/vocab/add", {
        user_id: userId,
        word: item.word,
        meaning: item.meaning,
        language: lesson.language,
        source: bookName || "scan",
      });
      setSavedWords((prev) => new Set(prev).add(item.word));
    } catch (error) {
      console.warn("Could not save word:", error);
    }
  };

  const saveAllWords = async () => {
    for (const item of currentTeaching.vocabulary || []) {
      await saveWord(item);
    }
  };

  // ================= Audio / Teaching =================

  const stopAudio = () => {
    readToken.current += 1;
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }
    if (resolveRef.current) {
      resolveRef.current();
      resolveRef.current = null;
    }
    setReadingSection(null);
    setAudioLoading(false);
  };

  const speak = async (text, language, token) => {
    const clean = speechText(text);
    if (!clean || token !== readToken.current) return;

    try {
      const response = await api.post("/audio/read", { text: clean, language });
      if (token !== readToken.current) return;

      const player = new Audio(audioUrl(response.data.audio));
      player.playbackRate = readingSpeed;
      audioRef.current = player;

      await new Promise((resolve) => {
        resolveRef.current = resolve;
        player.onended = resolve;
        player.onerror = resolve;
        player.play().catch(resolve);
      });
    } catch (error) {
      console.warn("speak failed:", error);
    }
  };

  const readTeaching = async (index, token) => {
    const teaching = steps[index]?.teaching;
    if (!teaching) return;

    const alive = () => token === readToken.current;

    if (teaching.translation) {
      setReadingSection("translation");
      await speak(teaching.translation, explainLanguage, token);
      if (!alive()) return;
      await wait(PAUSE.translation);
    }

    if (Array.isArray(teaching.vocabulary) && teaching.vocabulary.length) {
      setReadingSection("vocabulary");
      for (const word of teaching.vocabulary) {
        if (!alive()) return;
        await speak(`${word.word}. ${word.meaning}`, explainLanguage, token);
        await wait(PAUSE.vocabulary);
      }
    }

    if (alive() && teaching.grammar) {
      setReadingSection("grammar");
      await speak(teaching.grammar, explainLanguage, token);
      if (!alive()) return;
      await wait(PAUSE.grammar);
    }

    if (Array.isArray(teaching.examples) && teaching.examples.length) {
      setReadingSection("examples");
      for (const ex of teaching.examples) {
        if (!alive()) return;
        await speak(ex.sentence, lesson.language, token);
        await wait(500);
        if (!alive()) return;
        await speak(ex.translation, explainLanguage, token);
        await wait(PAUSE.example);
      }
    }

    if (alive() && teaching.practice) {
      setReadingSection("practice");
      await speak(String(teaching.practice), explainLanguage, token);
      await wait(PAUSE.practice);
    }
  };

  // ================= Navigation =================

  const nextSentence = () => {
    if (currentSentence >= sentences.length - 1) return;
    stopAudio();
    setChangingPage(true);
    setTimeout(() => {
      setCurrentSentence((prev) => prev + 1);
      setChangingPage(false);
    }, 250);
  };

  const previousSentence = () => {
    if (currentSentence <= 0) return;
    stopAudio();
    setChangingPage(true);
    setTimeout(() => {
      setCurrentSentence((prev) => prev - 1);
      setChangingPage(false);
    }, 250);
  };

  const playAudio = async (index = currentSentence) => {
    if (!lesson || !steps.length) return;

    stopAudio();
    const token = ++readToken.current;

    try {
      setAudioLoading(true);
      setReadingSection("sentence");

      await speak(steps[index].sentence, lesson.language, token);
      setAudioLoading(false);
      if (token !== readToken.current) return;

      await readTeaching(index, token);
      if (token !== readToken.current) return;

      setReadingSection(null);
      if (autoMode && index < steps.length - 1) nextSentence();
    } finally {
      if (token === readToken.current) setAudioLoading(false);
    }
  };

  const goToPage = async (targetPage) => {
    if (targetPage < 1 || targetPage > totalPages) return;

    stopAudio();

    try {
      const data = await fetchLessonPage(book, targetPage, profile);

      applyLesson(data, targetPage);
      setSpeakingResult(null);
      setXpGained(0);
      resetRecording();
      setPageUnlocked(false);

      if (book?.file_name) {
        api
          .post("/book/page", {
            user_id: userId,
            book_name: bookName,
            page: targetPage,
          })
          .catch(() => {});
      }

      await loadPageStatus(targetPage);
      await loadBookProgress(totalPages);
    } catch (error) {
      console.error("Page change failed:", error);
      alert(
        error?.response?.data?.error ||
          "Couldn't load that page. Please try again.",
      );
    }
  };

  const goToSpeakingPractice = () => {
    stopAudio();
    setAutoMode(false);

    if (sentences.length && currentSentence < sentences.length - 1) {
      setCurrentSentence(sentences.length - 1);
    }

    setScrollToSpeaking(true);
  };

  // ================= Effects =================
  // All effects live BELOW the functions they call.

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadLesson();
    return () => {
      readToken.current += 1;
      if (audioRef.current) audioRef.current.pause();
      if (recordedURLRef.current) URL.revokeObjectURL(recordedURLRef.current);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    if (autoMode && currentSentence !== 0) playAudio(currentSentence);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [currentSentence]);

  useEffect(() => {
    const element = sentenceRefs.current[currentSentence];
    if (element)
      element.scrollIntoView({ behavior: "smooth", block: "center" });
  }, [currentSentence]);

  useEffect(() => {
    if (!scrollToSpeaking) return;
    const element = speakingSectionRef.current;
    if (element) {
      element.scrollIntoView({ behavior: "smooth", block: "start" });
     
      setScrollToSpeaking(false);
    }
  }, [scrollToSpeaking, currentSentence, steps.length]);

  // ================= Render =================

  if (loading) return <Loader label="Preparing your AI lesson..." />;
  if (!lesson) return <Loader label={loadError || "Failed to load lesson."} />;

  const progressPercent = sentences.length
    ? ((currentSentence + 1) / sentences.length) * 100
    : 0;

  const isLastStep =
    sentences.length > 0 && currentSentence >= sentences.length - 1;
  const canContinue = pageUnlocked || !bookName;
  const isLastPage = page === totalPages;

  return (
    <div className="lesson-page" data-theme={theme}>
      <div className="lesson-hero">
        <button className="back-btn" onClick={() => navigate(-1)}>
          ←
        </button>

        {bookName && (
          <div className="book-progress-card">
            <h3>📘 Book Progress</h3>
            <p>
              {completedPages} / {totalPages} Pages Mastered
            </p>
            <div className="progress-track">
              <div
                className="progress-fill"
                style={{ width: `${(completedPages / totalPages) * 100}%` }}
              />
            </div>
          </div>
        )}

        <div>
          <span className="lesson-level">
            {lesson.language} • {profile?.learner_level}
          </span>
          <p className="page-indicator">
            Page {page} of {totalPages}
          </p>
        </div>

        <div className="hero-icon-actions">
          <button
            className="sleep-icon-btn"
            onClick={() => navigate("/sleep-mode")}
            aria-label="Open Sleep Teacher"
            title="Sleep Teacher"
          >
            😴
          </button>
          <button
            className="theme-toggle"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === "light" ? "dark" : "light"} mode`}
          >
            {theme === "light" ? "🌙" : "☀️"}
          </button>
        </div>
      </div>

      {lesson.notice && <div className="notice-banner">ℹ️ {lesson.notice}</div>}

      <div className="passage-card">
        <div className={`reading-flag ${readingSection ? "" : "idle"}`}>
          <span className="dot" />
          <span>
            {readingSection
              ? `Reading now: ${READING_LABELS[readingSection]}`
              : "Not reading"}
          </span>
        </div>

        <div className="reading-progress">
          <div
            className="reading-progress-fill"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        <div
          className={`reading-passage ${changingPage ? "page-changing" : ""}`}
        >
          <div
            ref={(el) => (sentenceRefs.current[currentSentence] = el)}
            className={`active-sentence ${readingSection === "sentence" ? "reading-highlight" : ""}`}
          >
            <span>{sentences[currentSentence]}</span>
            <button
              className="speaker-btn"
              onClick={() => playAudio(currentSentence)}
              aria-label="Read this phrase aloud"
            >
              🔊
            </button>
          </div>
        </div>

        <p className="sentence-progress">
          Lesson Step {sentences.length ? currentSentence + 1 : 0} /{" "}
          {sentences.length}
        </p>

        <div className="transport">
          <button onClick={previousSentence} disabled={currentSentence === 0}>
            ← Previous
          </button>
          <button
            className="play-btn"
            onClick={() => playAudio(currentSentence)}
            disabled={audioLoading}
          >
            ▶ Read
          </button>
          <button
            onClick={nextSentence}
            disabled={currentSentence >= sentences.length - 1}
          >
            Next →
          </button>
        </div>

        <div className="sub-controls">
          <button onClick={() => playAudio(currentSentence)}>🔁 Repeat</button>
          <button
            className={autoMode ? "active-auto" : ""}
            onClick={() => setAutoMode(!autoMode)}
          >
            {autoMode ? "🤖 Auto ON" : "🤖 Auto OFF"}
          </button>
          <select
            value={readingSpeed}
            onChange={(e) => setReadingSpeed(Number(e.target.value))}
          >
            <option value={0.75}>0.75×</option>
            <option value={1}>1×</option>
            <option value={1.25}>1.25×</option>
            <option value={1.5}>1.5×</option>
          </select>
        </div>
      </div>

      {currentTeaching.error && (
        <div className="section-card" style={{ borderColor: "#ef4444" }}>
          <h3>⚠️ This step failed to generate</h3>
          <p>{currentTeaching.error}</p>
        </div>
      )}

      <div className="lesson-grid">
        <div
          className={`info-card ${readingSection === "translation" ? "reading-highlight" : ""}`}
        >
          <h4>🌐 Translation</h4>
          <p>{currentTeaching.translation || "—"}</p>
        </div>

        {/* XP is given by the server when the page is passed */}
        <div className="info-card">
          <h4>🏆 Reward</h4>
          <h3>
            {pageUnlocked
              ? `✅ ${xpGained ? `+${xpGained} XP` : "Mastered"}`
              : "+25 XP"}
          </h3>
        </div>
      </div>

      <div
        className={`section-card ${readingSection === "vocabulary" ? "reading-highlight" : ""}`}
      >
        <h3>📚 Vocabulary</h3>
        <VocabularyGrid
          vocabulary={currentTeaching.vocabulary || []}
          saved={savedWords}
          onSave={saveWord}
        />
        {(currentTeaching.vocabulary || []).length > 0 && (
          <button className="save-all-btn" onClick={saveAllWords}>
            ＋ Save all words to flashcards
          </button>
        )}
      </div>

      <div
        className={`section-card ${readingSection === "grammar" ? "reading-highlight" : ""}`}
      >
        <h3>📝 Grammar</h3>
        <p>{currentTeaching.grammar || "—"}</p>
      </div>

      <div
        className={`section-card ${readingSection === "examples" ? "reading-highlight" : ""}`}
      >
        <h3>💬 Examples</h3>
        <ExampleList examples={currentTeaching.examples || []} />
      </div>

      <div
        className={`section-card ${readingSection === "practice" ? "reading-highlight" : ""}`}
      >
        <h3>🎯 Practice</h3>
        <PracticeBlock
          key={`${page}-${currentSentence}`}
          practice={currentTeaching.practice}
        />
      </div>

      {isLastStep && (
        <div className="section-card" ref={speakingSectionRef}>
          <div className="page-navigation">
            <button onClick={() => goToPage(page - 1)} disabled={page === 1}>
              ← Previous Page
            </button>

            {isLastPage ? (
              <button
                className={canContinue ? "next-unlocked" : "next-locked"}
                onClick={() => navigate("/library")}
                disabled={!canContinue}
              >
                {canContinue ? "🎉 Finish" : "🔒 Pass Speaking Practice"}
              </button>
            ) : (
              <button
                className={canContinue ? "next-unlocked" : "next-locked"}
                onClick={() => goToPage(page + 1)}
                disabled={!canContinue}
              >
                {canContinue ? "Next Page →" : "🔒 Pass Speaking Practice"}
              </button>
            )}
          </div>

          <h3>🎙️ AI Speaking Practice</h3>

          {canScore ? (
            <>
              <p>Listen → Repeat → Record → Get AI feedback</p>

              <div className="practice-actions">
                {!recording ? (
                  <button className="record-btn" onClick={startRecording}>
                    🎤 Start Recording
                  </button>
                ) : (
                  <button
                    className="record-btn recording"
                    onClick={stopRecording}
                  >
                    ⏹ Stop Recording
                  </button>
                )}

                <button onClick={playRecording} disabled={!recordedURL}>
                  ▶ Play Recording
                </button>

                <button
                  className="analyze-btn"
                  onClick={analyzePronunciation}
                  disabled={!recordedURL || analyzing}
                >
                  {analyzing ? "Analyzing..." : "✨ Analyze"}
                </button>
              </div>

              {recording && (
                <div className="recording-status">🔴 Recording...</div>
              )}

              {speakingResult && (
                <div className="score-card">
                  {speakingResult.score == null ? (
                    <p>{speakingResult.feedback}</p>
                  ) : (
                    <>
                      <h2>{speakingResult.score} / 100</h2>
                      <p className="score-grade">
                        {speakingResult.score >= 95
                          ? "🌟 Native-like"
                          : speakingResult.score >= 90
                            ? "Excellent"
                            : speakingResult.score >= PASS_SCORE
                              ? "Good"
                              : "Needs Practice"}
                      </p>

                      <div className="score-fill-track">
                        <div
                          className="score-fill"
                          style={{
                            width: `${speakingResult.score}%`,
                            background:
                              speakingResult.score >= 90
                                ? "var(--l-success)"
                                : speakingResult.score >= PASS_SCORE
                                  ? "var(--l-warning)"
                                  : "var(--l-danger)",
                          }}
                        />
                      </div>

                      {pageUnlocked ? (
                        <div className="unlock-success">
                          <h3>🔓 Page Unlocked!</h3>
                          <p>You passed this page. You can continue.</p>
                        </div>
                      ) : (
                        <div className="unlock-warning">
                          <h3>🔒 Next Page Locked</h3>
                          <p>
                            Score at least {PASS_SCORE} in speaking practice to
                            continue.
                          </p>
                        </div>
                      )}

                      <p>{speakingResult.feedback}</p>
                    </>
                  )}
                </div>
              )}
            </>
          ) : (
            <>
              <p>
                Speaking scores are not available for {lesson.language} yet.
                Listen to the audio, repeat each sentence aloud, then confirm
                below.
              </p>
              {bookName && (
                <button
                  className="analyze-btn"
                  onClick={markPracticed}
                  disabled={pageUnlocked}
                >
                  {pageUnlocked
                    ? "✅ Marked as practiced"
                    : "I practiced this page"}
                </button>
              )}
            </>
          )}
        </div>
      )}

      <div className="lesson-actions">
        <button className="practice-btn" onClick={goToSpeakingPractice}>
          🎙️ Speaking Practice
        </button>

        <button
          className="practice-btn"
          onClick={() => navigate("/flashcards")}
        >
          🧠 Review Flashcards
        </button>

        {book?.file_name &&
          !isScan &&
          (bookCompleted ? (
            <button className="exam-btn" onClick={() => navigate("/book-exam")}>
              🎓 Start Final Book Exam
            </button>
          ) : (
            <button disabled className="exam-btn locked">
              🔒 Complete Every Page First
            </button>
          ))}
      </div>
    </div>
  );
}

/* ---------------- Vocabulary ---------------- */

function VocabularyGrid({ vocabulary, saved, onSave }) {
  if (!Array.isArray(vocabulary)) return <p>{String(vocabulary)}</p>;

  return (
    <div className="vocabulary-grid">
      {vocabulary.map((item, index) => (
        <div key={index} className="vocabulary-item">
          <strong>{item.word}</strong>
          <span>{item.meaning}</span>
          <button
            className="save-word-btn"
            onClick={() => onSave(item)}
            disabled={saved.has(item.word)}
          >
            {saved.has(item.word) ? "✓ Saved" : "＋ Save"}
          </button>
        </div>
      ))}
    </div>
  );
}

/* ---------------- Examples ---------------- */

function ExampleList({ examples }) {
  if (!Array.isArray(examples)) return <p>{String(examples)}</p>;

  return (
    <div className="example-list">
      {examples.map((item, index) => (
        <div key={index} className="example-item">
          <p>{item.sentence}</p>
          <small>{item.translation}</small>
        </div>
      ))}
    </div>
  );
}

/* ---------------- Practice ---------------- */

function PracticeBlock({ practice }) {
  const [revealed, setRevealed] = useState(false);
  const [userAnswer, setUserAnswer] = useState("");
  const [checked, setChecked] = useState(false);

  if (!practice) return <p>No practice question for this step.</p>;

  const match = String(practice).match(
    /^([\s\S]*)\(Answer:\s*([\s\S]+?)\)\s*$/,
  );
  const questionText = match ? match[1].trim() : String(practice);
  const correctAnswer = match ? match[2].trim() : null;

  const isSpeakingPrompt = /\b(say|speak|pronounce)\b/i.test(questionText);

  const normalize = (s) =>
    (s || "")
      .toLowerCase()
      .trim()
      .replace(/[.,!?！？。、]/g, "");

  const isCorrect =
    checked &&
    correctAnswer &&
    normalize(userAnswer) === normalize(correctAnswer);

  return (
    <div className="practice-block">
      <p>{questionText}</p>

      {isSpeakingPrompt ? (
        <p className="practice-hint">
          🎙️ Use the recording tools below to say your answer aloud and get AI
          pronunciation feedback.
        </p>
      ) : (
        <div className="practice-input">
          <textarea
            value={userAnswer}
            onChange={(e) => {
              setUserAnswer(e.target.value);
              setChecked(false);
            }}
            placeholder="Type your answer..."
            rows={2}
          />

          <div className="practice-input-actions">
            <button
              onClick={() => setChecked(true)}
              disabled={!userAnswer.trim()}
            >
              Check Answer
            </button>
            {!revealed && (
              <button className="reveal-btn" onClick={() => setRevealed(true)}>
                Reveal Answer
              </button>
            )}
          </div>

          {checked && correctAnswer && (
            <p
              className={isCorrect ? "practice-correct" : "practice-incorrect"}
            >
              {isCorrect
                ? "✅ Correct!"
                : "❌ Not quite — try again or reveal the answer."}
            </p>
          )}
        </div>
      )}

      {revealed && correctAnswer && (
        <p style={{ fontWeight: 700 }}>✅ {correctAnswer}</p>
      )}
    </div>
  );
}
