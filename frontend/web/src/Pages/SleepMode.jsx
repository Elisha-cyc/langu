// frontend/web/src/Pages/SleepMode.jsx
import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

const TIMER_OPTIONS = [
  { label: "Off", minutes: 0 },
  { label: "15 min", minutes: 15 },
  { label: "30 min", minutes: 30 },
  { label: "1 hr", minutes: 60 },
];

const READING_LABELS = {
  sentence: "the phrase",
  translation: "the translation",
  vocabulary: "the vocabulary",
  grammar: "the grammar note",
  examples: "the examples",
};

const PAUSE = {
  afterSentence: 500,
  translation: 1500,
  vocabulary: 1200,
  grammar: 1500,
  example: 1000,
  afterStep: 800,
  afterPage: 1500,
};

// Add your own lullaby file at frontend/web/public/audio/lullaby.mp3
const LULLABY_URL = "/audio/lullaby.mp3";

function getStored(key) {
  try {
    return JSON.parse(localStorage.getItem(key));
  } catch {
    return null;
  }
}

// The profile is saved with "user_id" (Welcome) but older code read "id".
const userIdOf = (profile) => profile?.user_id ?? profile?.id ?? 1;

function audioUrl(path) {
  const base = (api.defaults?.baseURL || "http://127.0.0.1:5000").replace(
    /\/$/,
    "",
  );
  return `${base}/${String(path).replace(/^\//, "")}?t=${Date.now()}`;
}

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const MIN_LOADING_MS = 1200;

const ANIM_CSS = `
  @keyframes sleepFadeIn { from { opacity: 0; } to { opacity: 1; } }
  @keyframes sleepMoonRise {
    from { opacity: 0; transform: translateY(70px) scale(0.86); filter: blur(6px); }
    to { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
  }
  @keyframes sleepBreathe {
    0%, 100% { opacity: 0.7; transform: scale(0.96); }
    50% { opacity: 1; transform: scale(1.04); }
  }
  @keyframes sleepZ {
    0% { opacity: 0; transform: translate(0, 0) scale(0.7); }
    25% { opacity: 0.9; }
    100% { opacity: 0; transform: translate(26px, -46px) scale(1.15); }
  }
  @keyframes sleepDot {
    0%, 80%, 100% { opacity: 0.25; transform: translateY(0); }
    40% { opacity: 1; transform: translateY(-3px); }
  }

  .sleep-moon-wrap {
    display: flex;
    justify-content: center;
    animation: sleepMoonRise 1.8s cubic-bezier(0.2, 0.7, 0.2, 1) both;
  }
  .sleep-enter {
    animation: sleepFadeIn 1.2s ease-out both;
    animation-delay: var(--d, 0s);
  }

  .sleep-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    gap: 22px;
    text-align: center;
  }
  .sleep-loader { position: relative; width: 84px; height: 84px; }
  .sleep-loader-moon {
    width: 64px;
    height: 64px;
    border-radius: 50%;
    box-shadow: inset -18px -6px 0 0 #f4e9c8;
    filter: drop-shadow(0 0 16px rgba(244, 233, 200, 0.4));
    animation: sleepBreathe 3s ease-in-out infinite;
  }
  .sleep-loader-z {
    position: absolute;
    top: 6px;
    right: 2px;
    font-weight: 600;
    color: rgba(244, 233, 200, 0.9);
    opacity: 0;
    animation: sleepZ 3.6s ease-out infinite;
    animation-delay: var(--d, 0s);
  }
  .sleep-loading-text {
    margin: 0;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.95rem;
  }

  .sleep-dots { margin-left: 8px; white-space: nowrap; }
  .sleep-dots span {
    display: inline-block;
    width: 5px;
    height: 5px;
    margin: 0 2px;
    border-radius: 50%;
    background: currentColor;
    animation: sleepDot 1.2s ease-in-out infinite;
  }
  .sleep-dots span:nth-child(2) { animation-delay: 0.15s; }
  .sleep-dots span:nth-child(3) { animation-delay: 0.3s; }

  @media (prefers-reduced-motion: reduce) {
    .sleep-moon-wrap,
    .sleep-enter,
    .sleep-loader-moon,
    .sleep-dots span { animation: none; }
  }
`;

const INTRO_CSS = `
  .sleep-intro {
    position: relative;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
  }
  .sleep-intro-rise {
    display: flex;
    flex-direction: column;
    align-items: center;
    animation: sleepIntroRise 2.6s cubic-bezier(0.2, 0.7, 0.2, 1) both;
  }
  @keyframes sleepIntroRise {
    from { opacity: 0; transform: translateY(140px); }
    to { opacity: 1; transform: translateY(0); }
  }
  .sleep-intro-moon-wrap {
    position: relative;
    width: 120px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .sleep-intro-ring {
    position: absolute;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    border: 1.5px solid #f4e9c8;
    opacity: 0.1;
    animation: sleepIntroRing 6s ease-in-out 2.6s infinite;
  }
  @keyframes sleepIntroRing {
    0%, 100% { opacity: 0.1; transform: scale(0.85); }
    50% { opacity: 0.45; transform: scale(1.4); }
  }
  .sleep-intro-moon {
    width: 120px;
    height: 120px;
    border-radius: 50%;
    background: #f4e9c8;
    box-shadow: inset -34px -8px 0 0 #050816;
    filter: drop-shadow(0 0 24px rgba(244, 233, 200, 0.5));
    animation: sleepBreathe 4s ease-in-out infinite;
  }
  .sleep-intro-zs {
    position: absolute;
    top: 6px;
    right: -22px;
    width: 60px;
    height: 90px;
    pointer-events: none;
  }
  .sleep-intro-z {
    position: absolute;
    left: 0;
    top: 0;
    color: #f4e9c8;
    font-size: 22px;
    font-weight: 600;
    opacity: 0;
    animation: sleepZ 4.2s ease-out infinite;
    animation-delay: var(--d, 0s);
  }
  .sleep-intro-text {
    text-align: center;
    margin-top: 70px;
    padding: 0 30px;
    opacity: 0;
    animation: sleepFadeIn 1.8s ease-out 1.6s both;
  }
  .sleep-intro-title {
    color: #fff;
    font-size: 1.5rem;
    font-weight: 600;
    margin: 0;
  }
  .sleep-intro-sub {
    color: rgba(255, 255, 255, 0.6);
    margin-top: 10px;
    line-height: 1.5;
  }
  .sleep-intro-label {
    color: #f4e9c8;
    font-size: 1.1rem;
    margin-top: 34px;
    height: 26px;
    opacity: 0.85;
  }
  .sleep-intro-skip {
    position: absolute;
    bottom: 50px;
    background: none;
    border: none;
    padding: 12px;
    color: rgba(255, 255, 255, 0.45);
    font-size: 1rem;
    cursor: pointer;
  }

  @media (prefers-reduced-motion: reduce) {
    .sleep-intro-rise,
    .sleep-intro-ring,
    .sleep-intro-text { animation: none; opacity: 1; }
  }
`;

function SleepIntro({ onDone }) {
  const [label, setLabel] = useState("");
  const audioRef = useRef(null);

  useEffect(() => {
    const audio = audioRef.current;
    if (audio) {
      audio.volume = 0.35;
      audio.play().catch(() => {});
    }

    const labelTimers = [2600, 5600, 8600, 11600].map((ms, i) =>
      setTimeout(() => setLabel(i % 2 ? "Breathe out…" : "Breathe in…"), ms),
    );

    const doneTimer = setTimeout(onDone, 2600 + 6000 * 2);

    return () => {
      labelTimers.forEach(clearTimeout);
      clearTimeout(doneTimer);

      // Use the copy made at the top of the effect, not audioRef.current.
      if (!audio) return;
      let v = audio.volume;
      const fade = setInterval(() => {
        v -= 0.05;
        if (v <= 0) {
          clearInterval(fade);
          audio.pause();
        } else {
          audio.volume = v;
        }
      }, 60);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="sleep-page">
      <style>{ANIM_CSS}</style>
      <style>{INTRO_CSS}</style>

      <audio ref={audioRef} src={LULLABY_URL} loop preload="auto" />

      <div className="sleep-stars" aria-hidden="true" />

      <div className="sleep-intro">
        <div className="sleep-intro-rise">
          <div className="sleep-intro-moon-wrap">
            <div className="sleep-intro-ring" aria-hidden="true" />
            <div className="sleep-intro-moon" aria-hidden="true" />
            <div className="sleep-intro-zs" aria-hidden="true">
              <span className="sleep-intro-z" style={{ "--d": "0s" }}>
                z
              </span>
              <span className="sleep-intro-z" style={{ "--d": "1.4s" }}>
                z
              </span>
              <span className="sleep-intro-z" style={{ "--d": "2.8s" }}>
                Z
              </span>
            </div>
          </div>

          <div className="sleep-intro-text">
            <p className="sleep-intro-title">Let's get comfortable</p>
            <p className="sleep-intro-sub">
              Put your phone down and close your eyes.
              <br />
              Just listen — we'll do the rest.
            </p>
          </div>
        </div>

        <p className="sleep-intro-label" aria-live="polite">
          {label}
        </p>

        <button className="sleep-intro-skip" onClick={onDone}>
          Skip
        </button>
      </div>
    </div>
  );
}

function splitPassageFallback(passage) {
  return (passage || "").split(/(?<=[。.!?！？])/).filter((s) => s.trim());
}

function normalizeSteps(content) {
  if (Array.isArray(content?.steps) && content.steps.length) {
    return content.steps.map((step) => ({
      sentence: step.sentence || step.text || "",
      teaching: step.teaching || {},
    }));
  }

  const fallback = splitPassageFallback(content?.passage || "");

  return fallback.map((sentence) => ({
    sentence,
    teaching: content?.teaching || {},
  }));
}

function buildStaticContent(book) {
  const vocabulary = (book.vocab || []).map(([jp, romaji, meaning]) => ({
    word: `${jp} (${romaji})`,
    meaning,
  }));

  const steps = (book.examples || []).map(([jp, romaji, translation]) => ({
    sentence: `${jp} — ${romaji}`,
    teaching: {
      translation,
      vocabulary,
      grammar: book.note,
      examples: [{ sentence: `${jp} — ${romaji}`, translation }],
    },
  }));

  return {
    passage: steps.map((step) => step.sentence).join(" "),
    steps,
  };
}

// "こんにちは — konnichiwa": only the Japanese part is spoken.
const speechText = (text) =>
  String(text || "")
    .split(" — ")[0]
    .trim();

function buildLines(step, readOnly) {
  if (!step) return [];

  const lines = [{ id: "sentence", label: "Phrase", text: step.sentence }];
  if (readOnly) return lines;

  const teaching = step.teaching || {};

  if (teaching.translation) {
    lines.push({
      id: "translation",
      label: "Translation",
      text: teaching.translation,
    });
  }

  if (Array.isArray(teaching.vocabulary)) {
    teaching.vocabulary.forEach((word, i) => {
      lines.push({
        id: `vocab-${i}`,
        label: i === 0 ? "Vocabulary" : "",
        text: word.word,
        sub: word.meaning,
      });
    });
  }

  if (teaching.grammar) {
    lines.push({ id: "grammar", label: "Grammar", text: teaching.grammar });
  }

  if (Array.isArray(teaching.examples)) {
    teaching.examples.forEach((example, i) => {
      lines.push({
        id: `example-${i}`,
        label: i === 0 ? "Examples" : "",
        text: example.sentence,
        sub: example.translation,
      });
    });
  }

  return lines;
}

export default function SleepMode() {
  const navigate = useNavigate();

  const [phase, setPhase] = useState("intro");

  const [book, setBook] = useState(null);
  const [profile, setProfile] = useState(null);
  const [ready, setReady] = useState(false);
  const [loadError, setLoadError] = useState("");

  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [steps, setSteps] = useState([]);
  const [currentStep, setCurrentStep] = useState(0);

  const [activity, setActivity] = useState("Ready when you are");
  const [readingSection, setReadingSection] = useState(null);
  const [activeId, setActiveId] = useState(null);
  const [buffering, setBuffering] = useState(false);
  const [entered, setEntered] = useState(false);
  const [running, setRunning] = useState(false);
  const [paused, setPaused] = useState(false);
  const [timerMinutes, setTimerMinutes] = useState(0);
  const [readOnly, setReadOnly] = useState(false);

  const audioRef = useRef(null);
  // Every full start gets a new number. A full stop bumps it, so any older
  // loop knows it is out of date and quits without touching the new one.
  const tokenRef = useRef(0);
  // True while paused: the audio is paused and the loop waits.
  const pausedRef = useRef(false);
  const resolveRef = useRef(null);
  const timerRef = useRef(null);
  const lyricsRef = useRef(null);
  const lineRefs = useRef({});

  // The language the explanations are REALLY written in. It is English when
  // the learner's native language is Twi (the AI cannot write Twi), so an
  // English explanation is never read with a Twi voice.
  const explainRef = useRef(null);

  // Cuts the current audio for good and invalidates any running loop.
  const halt = () => {
    tokenRef.current += 1;
    pausedRef.current = false;
    clearTimeout(timerRef.current);

    const player = audioRef.current;
    audioRef.current = null;
    if (player) {
      player.onended = null;
      player.pause();
    }

    const finish = resolveRef.current;
    resolveRef.current = null;
    if (finish) finish();
  };

  // ================= Stop / Pause / Resume =================

  // Full stop: nothing keeps playing.
  const stopSleep = (message = "Session stopped") => {
    halt();
    setRunning(false);
    setPaused(false);
    setReadingSection(null);
    setActivity(message);
  };

  // Pause: the audio stops right now, even in the middle of a sentence.
  const pauseSleep = () => {
    pausedRef.current = true;
    if (audioRef.current) audioRef.current.pause();
    setRunning(false);
    setPaused(true);
    setActivity("Paused");
  };

  const resumeSleep = () => {
    pausedRef.current = false;
    if (audioRef.current) audioRef.current.play().catch(() => {});
    setPaused(false);
    setRunning(true);
  };

  // Holds the loop here while paused.
  const holdWhilePaused = async (tok) => {
    while (pausedRef.current && tok === tokenRef.current) await wait(150);
  };

  useEffect(() => {
    if (!ready) return;
    const t = setTimeout(() => setEntered(true), 3500);
    return () => clearTimeout(t);
  }, [ready]);

  useEffect(() => {
    const box = lyricsRef.current;
    if (!box) return;

    const reduceMotion = window.matchMedia?.(
      "(prefers-reduced-motion: reduce)",
    )?.matches;
    const behavior = reduceMotion ? "auto" : "smooth";

    const el = activeId ? lineRefs.current[activeId] : null;

    if (!el) {
      box.scrollTo({ top: 0, behavior });
      return;
    }

    box.scrollTo({
      top: el.offsetTop - box.clientHeight / 2 + el.offsetHeight / 2,
      behavior,
    });
  }, [activeId]);

  // One place builds the request for any kind of book, so the first page and
  // every following page are always asked for the same way.
  const requestPage = async (bookData, userProfile, targetPage) => {
    const common = {
      page: targetPage,
      user_id: userIdOf(userProfile),
      language: userProfile.learning_language,
      target_language: userProfile.native_language,
      learner_level: userProfile.learner_level,
    };

    const response = bookData.file_name
      ? await api.post(
          "/teach/page",
          { book: bookData.file_name, ...common },
          { timeout: 180000 },
        )
      : await api.post(
          "/lesson/curriculum",
          { lesson_id: bookData.id, title: bookData.title, ...common },
          { timeout: 180000 },
        );

    explainRef.current = response.data.explained_in || null;

    return response.data;
  };

  const loadBook = async () => {
    const startedAt = Date.now();
    const finishLoading = async () => {
      const remaining = MIN_LOADING_MS - (Date.now() - startedAt);
      if (remaining > 0) await wait(remaining);
      setReady(true);
    };

    const currentBook = getStored("current_book");
    const userProfile = getStored("lingua_profile");

    setProfile(userProfile);

    if (!currentBook || !userProfile) {
      await finishLoading();
      return;
    }

    setBook(currentBook);

    try {
      if (currentBook.vocab) {
        // Built-in Japanese lesson: its meanings are written in English.
        explainRef.current = "English";

        const content = buildStaticContent(currentBook);
        setSteps(normalizeSteps(content));
        setTotalPages(1);
        setPage(1);
      } else if (currentBook.file_name) {
        const progress = getStored("sleep_progress");
        const startPage =
          progress && progress.book === currentBook.file_name
            ? progress.page
            : 1;

        const data = await requestPage(currentBook, userProfile, startPage);

        setSteps(normalizeSteps(data.content));
        setTotalPages(data.total_pages || 1);
        setPage(startPage);
      } else {
        const data = await requestPage(currentBook, userProfile, 1);

        setSteps(normalizeSteps(data.content));
        setTotalPages(data.total_pages || 1);
        setPage(data.page || 1);
      }
    } catch (error) {
      console.error("Sleep Teacher load error:", error);
      setLoadError(
        error?.response?.data?.error ||
          "Couldn't load this book. Please try again.",
      );
    } finally {
      await finishLoading();
    }
  };

  const fetchPageSteps = async (targetPage) => {
    if (book.vocab) {
      return {
        steps: normalizeSteps(buildStaticContent(book)),
        total_pages: 1,
      };
    }

    const data = await requestPage(book, profile, targetPage);

    return {
      steps: normalizeSteps(data.content),
      total_pages: data.total_pages || totalPages,
    };
  };

  // ================= Audio =================

  // Plays one piece. Returns when it finishes, or on a full stop.
  const speak = async (text, language, lineId, tok) => {
    const clean = speechText(text);
    if (!clean || tok !== tokenRef.current) return;

    setBuffering(true);

    try {
      const response = await api.post("/audio/read", {
        text: clean,
        language,
        calm: true,
      });
      if (tok !== tokenRef.current) return;

      // If Stop was pressed while the audio was downloading, wait here.
      await holdWhilePaused(tok);
      if (tok !== tokenRef.current) return;

      await new Promise((resolve) => {
        const player = new Audio(audioUrl(response.data.audio));
        audioRef.current = player;
        resolveRef.current = resolve;

        player.onplaying = () => {
          setBuffering(false);
          if (lineId && tok === tokenRef.current) setActiveId(lineId);
        };
        player.onended = resolve;
        player.onerror = resolve;
        player.play().catch(resolve);
      });

      // The clip is over: forget it, so Resume never replays a finished clip.
      if (tok === tokenRef.current) {
        audioRef.current = null;
        resolveRef.current = null;
      }
    } catch (error) {
      console.warn("speak failed:", error);
    } finally {
      setBuffering(false);
    }
  };

  const readStep = async (step, nativeLanguage, passageLanguage, tok) => {
    if (!step || tok !== tokenRef.current) return;

    const alive = () => tok === tokenRef.current;

    // One piece: waits if paused, speaks, then pauses for a moment.
    const piece = async (text, language, lineId, after) => {
      await holdWhilePaused(tok);
      if (!alive()) return false;
      await speak(text, language, lineId, tok);
      if (!alive()) return false;
      await wait(after);
      return alive();
    };

    setReadingSection("sentence");
    setActivity("Reading the phrase");
    if (
      !(await piece(
        step.sentence,
        passageLanguage,
        "sentence",
        PAUSE.afterSentence,
      ))
    )
      return;

    if (readOnly) {
      setReadingSection(null);
      await wait(PAUSE.afterStep);
      return;
    }

    const teaching = step.teaching || {};

    if (teaching.translation) {
      setReadingSection("translation");
      setActivity("Explaining the translation");
      if (
        !(await piece(
          teaching.translation,
          nativeLanguage,
          "translation",
          PAUSE.translation,
        ))
      )
        return;
    }

    if (Array.isArray(teaching.vocabulary) && teaching.vocabulary.length) {
      setReadingSection("vocabulary");
      setActivity("Explaining vocabulary");
      for (let i = 0; i < teaching.vocabulary.length; i++) {
        const word = teaching.vocabulary[i];
        if (
          !(await piece(
            `${word.word}. ${word.meaning}`,
            nativeLanguage,
            `vocab-${i}`,
            PAUSE.vocabulary,
          ))
        )
          return;
      }
    }

    if (teaching.grammar) {
      setReadingSection("grammar");
      setActivity("Explaining the grammar note");
      if (
        !(await piece(
          teaching.grammar,
          nativeLanguage,
          "grammar",
          PAUSE.grammar,
        ))
      )
        return;
    }

    if (Array.isArray(teaching.examples) && teaching.examples.length) {
      setReadingSection("examples");
      setActivity("Reading the examples");
      for (let i = 0; i < teaching.examples.length; i++) {
        const example = teaching.examples[i];
        if (
          !(await piece(example.sentence, passageLanguage, `example-${i}`, 500))
        )
          return;
        if (
          !(await piece(
            example.translation,
            nativeLanguage,
            `example-${i}`,
            PAUSE.example,
          ))
        )
          return;
      }
    }

    setReadingSection(null);
  };

  // ================= Start =================

  const startSleepSession = async () => {
    if (!steps.length || !book || !profile) return;

    halt(); // make sure nothing old is still running
    const tok = tokenRef.current;
    const alive = () => tok === tokenRef.current;

    setPaused(false);
    setRunning(true);

    if (timerMinutes > 0) {
      timerRef.current = setTimeout(
        () => stopSleep("Timer finished. Sleep well 😴"),
        timerMinutes * 60 * 1000,
      );
    }

    const passageLanguage = profile.learning_language;

    let currentPage = page;
    let currentSteps = steps;
    // Resume from the step that was playing when the session was stopped.
    let firstStep = currentStep;

    try {
      while (alive() && currentPage <= totalPages) {
        if (currentPage !== page || !currentSteps) {
          const data = await fetchPageSteps(currentPage);
          if (!alive()) return;
          currentSteps = data.steps;
          setTotalPages(data.total_pages);
        }

        setPage(currentPage);
        setSteps(currentSteps);

        if (book.file_name) {
          localStorage.setItem(
            "sleep_progress",
            JSON.stringify({
              book: book.file_name,
              page: currentPage,
              totalPages,
            }),
          );
        }

        // Read AFTER the page is loaded, so the voice always matches the
        // language the explanations really came back in.
        const nativeLanguage = explainRef.current || profile.native_language;

        for (let i = firstStep; i < currentSteps.length; i++) {
          if (!alive()) return;

          setCurrentStep(i);
          setActiveId(null);
          await readStep(currentSteps[i], nativeLanguage, passageLanguage, tok);
        }

        if (!alive()) return;

        firstStep = 0;

        setActivity("Moving to the next page");
        await wait(PAUSE.afterPage);
        if (!alive()) return;

        currentPage++;
        currentSteps = null;
        setCurrentStep(0);
      }

      if (alive() && currentPage > totalPages) {
        clearTimeout(timerRef.current);
        setActivity("Session finished. Sleep well 😴");
      }
    } catch (error) {
      console.error("Sleep session error:", error);
      if (alive()) {
        setActivity(
          error?.response?.data?.error ||
            "Something went wrong. Try again in a moment.",
        );
      }
    } finally {
      // Only the loop that is still current may reset the buttons.
      if (alive()) {
        setRunning(false);
        setPaused(false);
        setReadingSection(null);
      }
    }
  };

  // ================= Load book + cleanup =================
  // Declared AFTER loadBook and halt, and BEFORE the early returns below.

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadBook();

    return () => halt();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ================= Render =================

  if (phase === "intro") {
    return <SleepIntro onDone={() => setPhase("main")} />;
  }

  if (!ready) {
    return (
      <div className="sleep-page">
        <style>{ANIM_CSS}</style>

        <div className="sleep-stars" aria-hidden="true" />

        <div
          className="sleep-inner sleep-loading"
          role="status"
          aria-live="polite"
        >
          <div className="sleep-loader" aria-hidden="true">
            <div className="sleep-loader-moon" />
            <span className="sleep-loader-z" style={{ "--d": "0s" }}>
              z
            </span>
            <span className="sleep-loader-z" style={{ "--d": "1.2s" }}>
              z
            </span>
            <span className="sleep-loader-z" style={{ "--d": "2.4s" }}>
              Z
            </span>
          </div>
          <p className="sleep-loading-text">
            Preparing your lesson
            <span className="sleep-dots" aria-hidden="true">
              <span />
              <span />
              <span />
            </span>
          </p>
        </div>
      </div>
    );
  }

  const ec = entered ? "" : " sleep-enter";
  const ed = (seconds) => (entered ? undefined : { "--d": `${seconds}s` });

  const playing = running || paused;
  const title = book?.title || book?.file_name || "Your book";
  const percent = totalPages ? Math.min(100, (page / totalPages) * 100) : 0;
  const step = steps[currentStep];
  const lines = buildLines(step, readOnly);
  const activeIndex = lines.findIndex((line) => line.id === activeId);

  return (
    <div className="sleep-page">
      <style>{`
        .sleep-lyrics {
          position: relative;
          height: 46vh;
          overflow-y: auto;
          padding: 18vh 12px;
          text-align: center;
          scrollbar-width: none;
          -webkit-mask-image: linear-gradient(transparent, #000 20%, #000 80%, transparent);
          mask-image: linear-gradient(transparent, #000 20%, #000 80%, transparent);
        }
        .sleep-lyrics::-webkit-scrollbar { display: none; }

        .sleep-lyric {
          margin: 0 auto 22px;
          max-width: 34rem;
          color: rgba(255, 255, 255, 0.28);
          transform: scale(0.94);
          transition: color 0.5s ease, transform 0.5s ease;
        }
        .sleep-lyric-label {
          display: block;
          margin-bottom: 4px;
          font-size: 0.75rem;
          opacity: 0.8;
        }
        .sleep-lyric-text {
          margin: 0;
          font-size: 1.35rem;
          font-weight: 600;
          line-height: 1.4;
        }
        .sleep-lyric-sub {
          margin: 4px 0 0;
          font-size: 0.95rem;
          line-height: 1.4;
        }

        .sleep-lyric.is-done { color: rgba(255, 255, 255, 0.5); }

        .sleep-lyric.is-active {
          color: #fff;
          transform: scale(1);
        }

        .sleep-lyrics.is-idle .sleep-lyric {
          color: rgba(255, 255, 255, 0.7);
          transform: scale(1);
        }

        @media (prefers-reduced-motion: reduce) {
          .sleep-lyric { transition: none; }
        }
      `}</style>

      <style>{ANIM_CSS}</style>

      <div className="sleep-stars" aria-hidden="true" />

      <div className="sleep-inner">
        <header className="sleep-top">
          <button
            className="sleep-back"
            onClick={() => {
              stopSleep();
              navigate(-1);
            }}
            aria-label="Go back"
          >
            ←
          </button>
          <span className="sleep-badge">Sleep Teacher</span>
        </header>

        <div className="sleep-moon-wrap">
          <div
            className={`sleep-moon ${running ? "is-playing" : ""}`}
            aria-hidden="true"
          />
        </div>

        {!book || !steps.length ? (
          <div className="sleep-empty">
            <h1 className="sleep-title">Pick something to fall asleep to</h1>
            <p className="sleep-sub">
              {loadError ||
                "Choose a book in your Library and Sleep Teacher will read it to you."}
            </p>
            <button
              className="sleep-main-btn"
              onClick={() => navigate("/library")}
            >
              Open Library
            </button>
          </div>
        ) : (
          <>
            <h1 className={`sleep-title${ec}`} style={ed(0.6)}>
              {title}
            </h1>
            <p className={`sleep-sub${ec}`} style={ed(0.8)}>
              Page {page} of {totalPages} • Step {currentStep + 1} of{" "}
              {steps.length}
            </p>

            <div
              className={`sleep-progress${ec}`}
              style={ed(1.0)}
              role="progressbar"
              aria-valuemin={0}
              aria-valuemax={100}
              aria-valuenow={Math.round(percent)}
            >
              <div
                className="sleep-progress-fill"
                style={{ width: `${percent}%` }}
              />
            </div>

            <div className={`sleep-now${ec}`} style={ed(1.1)}>
              <span className="sleep-now-label">
                {running ? "Now playing" : "Status"}
              </span>
              <p className="sleep-now-text">
                {running && readingSection
                  ? `Reading now: ${READING_LABELS[readingSection]}`
                  : activity}
                {running && buffering && (
                  <span className="sleep-dots" aria-hidden="true">
                    <span />
                    <span />
                    <span />
                  </span>
                )}
              </p>
            </div>

            <div
              ref={lyricsRef}
              className={`sleep-lyrics ${
                playing || activeId ? "" : "is-idle"
              }${ec}`}
              style={ed(1.3)}
            >
              {lines.map((line, i) => {
                const state =
                  i === activeIndex
                    ? "is-active"
                    : activeIndex !== -1 && i < activeIndex
                      ? "is-done"
                      : "";

                return (
                  <div
                    key={`${page}-${currentStep}-${line.id}`}
                    ref={(el) => {
                      lineRefs.current[line.id] = el;
                    }}
                    className={`sleep-lyric ${state}`}
                    aria-current={i === activeIndex ? "true" : undefined}
                  >
                    {line.label && (
                      <span className="sleep-lyric-label">{line.label}</span>
                    )}
                    <p className="sleep-lyric-text">{line.text}</p>
                    {line.sub && <p className="sleep-lyric-sub">{line.sub}</p>}
                  </div>
                );
              })}
            </div>

            <div className={`sleep-timer${ec}`} style={ed(1.5)}>
              <span className="sleep-timer-label">What to play</span>
              <div className="sleep-chips">
                <button
                  className={`sleep-chip ${readOnly ? "active" : ""}`}
                  onClick={() => setReadOnly(true)}
                  disabled={playing}
                >
                  Just read
                </button>
                <button
                  className={`sleep-chip ${!readOnly ? "active" : ""}`}
                  onClick={() => setReadOnly(false)}
                  disabled={playing}
                >
                  Read + explain
                </button>
              </div>
            </div>

            <div className={`sleep-timer${ec}`} style={ed(1.6)}>
              <span className="sleep-timer-label">Stop after</span>
              <div className="sleep-chips">
                {TIMER_OPTIONS.map((opt) => (
                  <button
                    key={opt.minutes}
                    className={`sleep-chip ${
                      timerMinutes === opt.minutes ? "active" : ""
                    }`}
                    onClick={() => setTimerMinutes(opt.minutes)}
                    disabled={playing}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </div>

            {running ? (
              <button className="sleep-main-btn is-stop" onClick={pauseSleep}>
                Stop Session
              </button>
            ) : paused ? (
              <>
                <button className="sleep-main-btn" onClick={resumeSleep}>
                  Resume
                </button>
                <button
                  className="sleep-link"
                  onClick={() => stopSleep("Session ended")}
                >
                  End session
                </button>
              </>
            ) : (
              <button
                className={`sleep-main-btn${ec}`}
                style={ed(1.8)}
                onClick={startSleepSession}
              >
                {page > 1 || currentStep > 0
                  ? `Resume from page ${page}`
                  : "Start Sleep Session"}
              </button>
            )}

            <button
              className="sleep-link"
              onClick={() => {
                stopSleep();
                navigate("/library");
              }}
            >
              Change book
            </button>
          </>
        )}
      </div>
    </div>
  );
}
