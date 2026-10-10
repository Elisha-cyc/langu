// frontend/web/src/Pages/Library.jsx
import { useEffect, useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import {
  BookOpen,
  FolderOpen,
  FileText,
  Image as ImageIcon,
  Camera,
  Search,
} from "lucide-react";
import api from "../services/api";
import Loader from "../components/common/loader";
import { JAPANESE_LESSONS } from "../data/japaneseLessons";
import { getProfile, getUserId, topicLessons } from "../utils/lesson";

// Each language gets its own fallback when the library request fails.
function fallbackCourse(profile) {
  const language = (profile?.learning_language || "").toLowerCase();
  const level = (profile?.learner_level || "Beginner").toLowerCase();

  if (language === "japanese" && level === "beginner") return JAPANESE_LESSONS;

  return topicLessons(profile?.learner_level || "Beginner");
}

export default function Library() {
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState("official");
  const [officialBooks, setOfficialBooks] = useState([]);
  const [myBooks, setMyBooks] = useState([]);
  const [nativeBooks, setNativeBooks] = useState([]);
  const [profile, setProfile] = useState(null);
  const [importing, setImporting] = useState(false);

  const [onlineBooks, setOnlineBooks] = useState([]);
  const [onlineLoading, setOnlineLoading] = useState(false);
  const [onlineLoaded, setOnlineLoaded] = useState(false);
  const [onlinePage, setOnlinePage] = useState(1);
  const [hasMore, setHasMore] = useState(false);
  const [onlineNote, setOnlineNote] = useState("");
  const [onlineError, setOnlineError] = useState("");
  const [searchText, setSearchText] = useState("");
  const [activeQuery, setActiveQuery] = useState("");
  const [openingId, setOpeningId] = useState(null);
  const [savedBooks, setSavedBooks] = useState([]);

  const pdfInputRef = useRef(null);
  const imageInputRef = useRef(null);

  const loadLibrary = async () => {
    const userId = getUserId();
    let current = getProfile();
    setProfile(current);

    try {
      const profileRes = await api.get(`/profile/${userId}`);
      current = { ...current, ...profileRes.data };
      setProfile(current);
    } catch (error) {
      console.warn("Using the saved profile:", error);
    }

    try {
      const libraryRes = await api.get(`/library?user_id=${userId}`);
      const backendBooks = libraryRes.data.official_books || [];

      setOfficialBooks(
        backendBooks.length > 0 ? backendBooks : fallbackCourse(current),
      );
      setMyBooks(libraryRes.data.my_books || []);
      setNativeBooks(libraryRes.data.native_books || []);
    } catch (error) {
      console.error("Library error:", error);
      setOfficialBooks(fallbackCourse(current));
    } finally {
      setLoading(false);
    }
  };

  const reloadMyBooks = async () => {
    try {
      const res = await api.get(`/library?user_id=${getUserId()}`);
      setMyBooks(res.data.my_books || []);
    } catch (error) {
      console.error(error);
    }
  };

  // ---------- Internet library ----------
  const loadSaved = async () => {
    try {
      const res = await api.get("/library/online/saved", {
        params: { language: profile?.learning_language || "" },
      });
      setSavedBooks(res.data.results || []);
    } catch (error) {
      console.error("Saved books error:", error);
    }
  };

  const loadOnline = async ({ page, query, append }) => {
    setOnlineLoading(true);
    setOnlineError("");

    try {
      const res = await api.get("/library/online/search", {
        params: { language: profile?.learning_language || "", query, page },
        timeout: 45000,
      });

      const results = res.data.results || [];

      setOnlineBooks((prev) => {
        if (!append) return results;
        const seen = new Set(prev.map((b) => b.gutenberg_id));
        return [...prev, ...results.filter((b) => !seen.has(b.gutenberg_id))];
      });

      setHasMore(!!res.data.has_more);
      setOnlineNote(res.data.note || "");
      setOnlinePage(page);
      setActiveQuery(query);
    } catch (error) {
      setOnlineError(
        error?.response?.data?.error ||
          "Couldn't reach the online library. Check your connection.",
      );
    } finally {
      setOnlineLoading(false);
      setOnlineLoaded(true);
    }
  };

  const handleSearch = (event) => {
    event.preventDefault();
    loadOnline({ page: 1, query: searchText.trim(), append: false });
  };

  // ---------- Opening books ----------
  const startBook = (book, sleep = false) => {
    localStorage.setItem("current_book", JSON.stringify(book));
    // Makes the lesson page read this book, not an old camera scan.
    localStorage.setItem("study_source", "book");
    navigate(sleep ? "/sleep-mode" : "/lesson");
  };

  const openOnlineBook = async (book, sleep = false) => {
    try {
      setOpeningId(book.gutenberg_id);

      const res = await api.post(
        "/library/online/add",
        {
          language: profile?.learning_language,
          gutenberg_id: book.gutenberg_id,
          title: book.title,
          author: book.author,
        },
        { timeout: 90000 },
      );

      loadSaved();
      startBook(res.data, sleep);
    } catch (error) {
      alert(
        error?.response?.data?.error ||
          "Couldn't download that book. Please try again.",
      );
    } finally {
      setOpeningId(null);
    }
  };

  const openNativeBook = async (book, sleep = false) => {
    try {
      const res = await api.post("/library/native/open", {
        file_name: book.file_name,
        language: profile?.learning_language,
      });
      startBook(res.data, sleep);
    } catch (error) {
      alert(error?.response?.data?.error || "Couldn't open that book.");
    }
  };

  // ---------- Import ----------
  const handlePdfSelected = async (event) => {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;

    try {
      setImporting(true);
      const form = new FormData();
      form.append("book", file);

      await api.post("/library/import", form, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 120000,
      });

      await reloadMyBooks();
    } catch (error) {
      alert(error?.response?.data?.error || "Couldn't import that file.");
    } finally {
      setImporting(false);
    }
  };

  const handleImageSelected = async (event) => {
    const file = event.target.files?.[0];
    event.target.value = "";
    if (!file) return;

    try {
      setImporting(true);

      const form = new FormData();
      form.append("image", file);
      form.append("language", profile?.learning_language || "English");
      form.append("target_language", profile?.native_language || "English");
      form.append("learner_level", profile?.learner_level || "Beginner");
      form.append("user_id", getUserId());

      const response = await api.post("/scan", form, {
        headers: { "Content-Type": "multipart/form-data" },
        timeout: 180000,
      });

      localStorage.setItem(
        "generated_lesson",
        JSON.stringify(response.data.lesson),
      );
      localStorage.setItem("scan_text", response.data.page_text);
      if (response.data.audio)
        localStorage.setItem("scan_audio", response.data.audio);
      else localStorage.removeItem("scan_audio");
      localStorage.setItem("study_source", "scan");

      navigate("/study-mode");
    } catch (error) {
      alert(
        error?.response?.data?.error ||
          "Couldn't process that image. Please try again.",
      );
    } finally {
      setImporting(false);
    }
  };

  // ================= Effects =================
  // Declared AFTER the functions they call.

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    loadLibrary();
    
  }, []);

  useEffect(() => {
    if (activeTab === "native" && profile) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      loadSaved();
      if (!onlineLoaded && !onlineLoading) {

        loadOnline({ page: 1, query: "", append: false });
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTab, profile]);

  // ================= Render =================

  if (loading) return <Loader label="Loading Library..." />;

  const BookCard = ({ book, icon = "📖", actions }) => (
    <div className="book-card">
      <div className="book-cover">{icon}</div>
      <h3>{book.title}</h3>
      <p>
        {book.author ||
          (book.type ? `${book.type} • ${book.size_kb} KB` : book.level)}
      </p>
      <div className="book-card-actions">{actions}</div>
    </div>
  );

  return (
    <div className="library-page">
      <div className="library-header">
        <h1>Library</h1>
        {profile && (
          <p>
            {profile.learning_language} • {profile.learner_level}
          </p>
        )}
      </div>

      <div className="library-tabs">
        <button
          className={activeTab === "official" ? "active-tab" : ""}
          onClick={() => setActiveTab("official")}
        >
          📚 Official Course
        </button>
        <button
          className={activeTab === "native" ? "active-tab" : ""}
          onClick={() => setActiveTab("native")}
        >
          📖 {profile?.learning_language} Books
        </button>
        <button
          className={activeTab === "my" ? "active-tab" : ""}
          onClick={() => setActiveTab("my")}
        >
          📂 My Books
        </button>
      </div>

      {activeTab === "official" && (
        <div className="books-grid">
          {officialBooks.map((book) => (
            <BookCard
              key={book.id}
              book={{
                ...book,
                title: book.title,
                level: `Lesson ${book.id} • ${book.level}`,
              }}
              icon="📘"
              actions={
                <>
                  <button onClick={() => startBook(book)}>Start Lesson</button>
                  <button
                    className="sleep-btn"
                    onClick={() => startBook(book, true)}
                  >
                    😴 Sleep Teacher
                  </button>
                </>
              }
            />
          ))}
        </div>
      )}

      {activeTab === "native" && (
        <>
          <form className="library-search" onSubmit={handleSearch}>
            <input
              type="text"
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
              placeholder={`Search ${profile?.learning_language || ""} books by title or author`}
            />
            <button type="submit" disabled={onlineLoading}>
              <Search size={16} /> Search
            </button>
          </form>

          {nativeBooks.length > 0 && (
            <>
              <h2 className="library-section-title">On this device</h2>
              <div className="books-grid">
                {nativeBooks.map((book) => (
                  <BookCard
                    key={book.file_name}
                    book={book}
                    actions={
                      <>
                        <button onClick={() => openNativeBook(book)}>
                          Open Book
                        </button>
                        <button
                          className="sleep-btn"
                          onClick={() => openNativeBook(book, true)}
                        >
                          😴 Sleep Teacher
                        </button>
                      </>
                    }
                  />
                ))}
              </div>
            </>
          )}

          {savedBooks.length > 0 && (
            <>
              <h2 className="library-section-title">Downloaded</h2>
              <div className="books-grid">
                {savedBooks.map((book) => (
                  <BookCard
                    key={book.gutenberg_id}
                    book={{
                      ...book,
                      author: book.author || `${book.size_kb} KB`,
                    }}
                    actions={
                      <>
                        <button
                          onClick={() => openOnlineBook(book)}
                          disabled={openingId === book.gutenberg_id}
                        >
                          {openingId === book.gutenberg_id
                            ? "Opening…"
                            : "Study"}
                        </button>
                        <button
                          className="sleep-btn"
                          onClick={() => openOnlineBook(book, true)}
                          disabled={openingId === book.gutenberg_id}
                        >
                          😴 Sleep Teacher
                        </button>
                      </>
                    }
                  />
                ))}
              </div>
            </>
          )}

          <h2 className="library-section-title">
            {activeQuery
              ? `Results for “${activeQuery}”`
              : "Popular books online"}
          </h2>

          {onlineError && (
            <p className="library-note error">
              {onlineError}{" "}
              <button
                type="button"
                disabled={onlineLoading}
                onClick={() =>
                  loadOnline({ page: 1, query: activeQuery, append: false })
                }
              >
                Retry
              </button>
            </p>
          )}

          {!onlineError && onlineNote && (
            <p className="library-note">{onlineNote}</p>
          )}
          {onlineLoading && onlineBooks.length === 0 && (
            <p className="library-note">Loading books from the internet…</p>
          )}

          {onlineLoaded &&
            !onlineLoading &&
            !onlineError &&
            !onlineNote &&
            onlineBooks.length === 0 && (
              <div className="empty-library">
                <BookOpen size={60} />
                <h3>No books found</h3>
                <p>
                  Try a different search. The free online library has a smaller
                  selection for some languages.
                </p>
              </div>
            )}

          {onlineBooks.length > 0 && (
            <div className="books-grid">
              {onlineBooks.map((book) => (
                <BookCard
                  key={book.gutenberg_id}
                  book={book}
                  actions={
                    <>
                      <button
                        onClick={() => openOnlineBook(book)}
                        disabled={openingId === book.gutenberg_id}
                      >
                        {openingId === book.gutenberg_id
                          ? "Downloading…"
                          : "Study"}
                      </button>
                      <button
                        className="sleep-btn"
                        onClick={() => openOnlineBook(book, true)}
                        disabled={openingId === book.gutenberg_id}
                      >
                        😴 Sleep Teacher
                      </button>
                    </>
                  }
                />
              ))}
            </div>
          )}

          {hasMore && (
            <button
              className="load-more-btn"
              disabled={onlineLoading}
              onClick={() =>
                loadOnline({
                  page: onlinePage + 1,
                  query: activeQuery,
                  append: true,
                })
              }
            >
              {onlineLoading ? "Loading…" : "Load more"}
            </button>
          )}
        </>
      )}

      {activeTab === "my" && (
        <>
          <div className="library-action-cards">
            <button
              className="library-action-card"
              onClick={() => pdfInputRef.current?.click()}
              disabled={importing}
            >
              <FileText size={22} />
              <div className="library-action-card-content">
                <strong>Import PDF / DOCX</strong>
                <span>Choose from your device</span>
              </div>
            </button>
            <button
              className="library-action-card"
              onClick={() => imageInputRef.current?.click()}
              disabled={importing}
            >
              <ImageIcon size={22} />
              <div className="library-action-card-content">
                <strong>Upload Image</strong>
                <span>Gallery or Files</span>
              </div>
            </button>
            <button
              className="library-action-card"
              onClick={() => navigate("/scan")}
              disabled={importing}
            >
              <Camera size={22} />
              <div className="library-action-card-content">
                <strong>Scan with Camera</strong>
                <span>Live capture</span>
              </div>
            </button>
          </div>

          <input
            ref={pdfInputRef}
            type="file"
            accept=".pdf,.docx"
            style={{ display: "none" }}
            onChange={handlePdfSelected}
          />
          <input
            ref={imageInputRef}
            type="file"
            accept="image/*"
            style={{ display: "none" }}
            onChange={handleImageSelected}
          />

          {importing && <p className="library-note">Processing...</p>}

          {myBooks.length === 0 ? (
            <div className="empty-library">
              <FolderOpen size={60} />
              <h3>Your library is empty</h3>
              <p>
                Import a PDF or DOCX, or scan a page, to build your personal
                library.
              </p>
            </div>
          ) : (
            <div className="books-grid">
              {myBooks.map((book) => (
                <BookCard
                  key={book.file_name}
                  book={book}
                  icon="📄"
                  actions={
                    <>
                      <button onClick={() => startBook(book)}>Open Book</button>
                      <button
                        className="sleep-btn"
                        onClick={() => startBook(book, true)}
                      >
                        😴 Sleep Teacher
                      </button>
                    </>
                  }
                />
              ))}
            </div>
          )}
        </>
      )}
    </div>
  );
}
