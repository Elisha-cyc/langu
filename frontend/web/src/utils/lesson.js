// frontend/web/src/utils/lesson.js   (NEW: helpers shared by every page)
import api from "../services/api";

export function getStored(key) {
  try {
    return JSON.parse(localStorage.getItem(key));
  } catch {
    return null;
  }
}

export const getProfile = () => getStored("lingua_profile");

// The old pages read profile.id, but Welcome saved profile.user_id, so every
// request went out as user 1. This always finds the right id.
export function getUserId() {
  const profile = getProfile();
  const id = Number(
    profile?.user_id ?? profile?.id ?? localStorage.getItem("lingua_user"),
  );
  return Number.isFinite(id) && id > 0 ? id : 1;
}

export function getBookName(book) {
  const name = book?.file_name || book?.title || book?.id;
  return name ? String(name) : null;
}

export function audioUrl(path) {
  if (!path) return null;
  const base = (api.defaults?.baseURL || "http://127.0.0.1:5000").replace(
    /\/$/,
    "",
  );
  return `${base}/${String(path).replace(/^\//, "")}?t=${Date.now()}`;
}

// "こんにちは — konnichiwa" -> only the Japanese part is spoken
export const speechText = (text) =>
  String(text || "")
    .split(" — ")[0]
    .trim();

// Whisper cannot score Twi
export const scoringAvailable = (language) =>
  String(language || "")
    .trim()
    .toLowerCase() !== "twi";

export function normalizeSteps(content) {
  if (Array.isArray(content?.steps) && content.steps.length) {
    return content.steps.map((step) => ({
      sentence: step.sentence || step.text || "",
      teaching: step.teaching || {},
    }));
  }

  return (content?.passage || "")
    .split(/(?<=[。.!?！？])/)
    .filter((s) => s.trim())
    .map((sentence) => ({ sentence, teaching: content?.teaching || {} }));
}

// The built-in Japanese lessons carry their own vocab / examples / note.
export function buildStaticContent(book) {
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
      practice: "",
    },
  }));

  return { passage: steps.map((s) => s.sentence).join(" "), steps };
}

// Generic course for languages without curriculum files (the AI writes the passages)
export const TOPICS = [
  "Greetings",
  "Introducing Yourself",
  "Numbers 1–10",
  "Numbers 11–100",
  "Days of the Week",
  "Months of the Year",
  "Telling Time",
  "Family Members",
  "Colors",
  "Basic Adjectives",
  "Alphabet and Sounds",
  "Pronunciation Basics",
  "Common Nouns",
  "Pronouns",
  "Yes/No Questions",
  "Question Words",
  "Present Tense Verbs",
  "Past Tense Verbs",
  "Future Tense",
  "Negative Sentences",
  "This and That",
  "Prepositions of Place",
  "Food Vocabulary",
  "Ordering at a Restaurant",
  "Shopping Phrases",
  "Asking for Directions",
  "Transportation",
  "Weather",
  "The Four Seasons",
  "Body Parts",
  "Daily Routine",
  "Hobbies and Free Time",
  "School Vocabulary",
  "Work and Jobs",
  "Animals",
  "Emotions and Feelings",
  "Polite Requests",
  "Counting Objects",
  "Making Comparisons",
  "Making Plans and Invitations",
  "At the Hotel",
  "At the Doctor",
  "At the Airport",
  "Talking on the Phone",
  "Describing People",
  "Describing Places",
  "Giving Opinions",
  "Telling a Story",
  "Common Idioms",
  "Everyday Conversation",
];

export const topicLessons = (level) =>
  TOPICS.map((title, i) => ({ id: i + 1, title, level }));

// One function opens any kind of book. The server finds imported PDFs,
// DOCX files and downloaded online books by their file name.
export async function fetchLessonPage(book, page = 1, profile = getProfile()) {
  const common = {
    page,
    user_id: getUserId(),
    language: profile.learning_language,
    target_language: profile.native_language,
    learner_level: profile.learner_level,
  };

  const url = book?.file_name ? "/teach/page" : "/lesson/curriculum";

  const body = book?.file_name
    ? { book: book.file_name, ...common }
    : { lesson_id: book.id, title: book.title, ...common };

  const response = await api.post(url, body, { timeout: 180000 });
  return response.data;
}
