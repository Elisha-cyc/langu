# backend/database/models.py   (REPLACES the batch-1 version: 3 new tables)
CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    native_language TEXT NOT NULL,
    learning_language TEXT NOT NULL,
    learner_level TEXT DEFAULT 'Beginner',
    xp INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_LESSONS_TABLE = """
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    language TEXT NOT NULL,
    content TEXT NOT NULL,
    difficulty TEXT DEFAULT 'Beginner',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

CREATE_PROGRESS_TABLE = """
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    lessons_completed INTEGER DEFAULT 0,
    correct_answers INTEGER DEFAULT 0,
    incorrect_answers INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
"""

CREATE_READING_PROGRESS_TABLE = """
CREATE TABLE IF NOT EXISTS reading_progress (
    user_id INTEGER NOT NULL,
    book_name TEXT NOT NULL,
    current_page INTEGER DEFAULT 1,
    PRIMARY KEY(user_id, book_name),
    FOREIGN KEY(user_id) REFERENCES users(id)
)
"""

CREATE_OFFICIAL_BOOKS_TABLE = """
CREATE TABLE IF NOT EXISTS official_books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    language TEXT NOT NULL,
    level TEXT NOT NULL,
    author TEXT,
    cover TEXT,
    file_name TEXT NOT NULL
)
"""

CREATE_BOOK_MEMORY_TABLE = """
CREATE TABLE IF NOT EXISTS book_memory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    book_title TEXT,
    language TEXT,
    current_page INTEGER,
    context TEXT,
    UNIQUE(user_id, book_title)
)
"""

CREATE_PAGE_MASTERY_TABLE = """
CREATE TABLE IF NOT EXISTS page_mastery (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_name TEXT NOT NULL,
    page_number INTEGER NOT NULL,
    score INTEGER DEFAULT 0,
    passed INTEGER DEFAULT 0,
    UNIQUE(user_id, book_name, page_number)
)
"""

# NEW: saved words for spaced-repetition flashcards
CREATE_VOCABULARY_TABLE = """
CREATE TABLE IF NOT EXISTS vocabulary (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    word TEXT NOT NULL,
    meaning TEXT DEFAULT '',
    language TEXT NOT NULL,
    source TEXT DEFAULT '',
    ease REAL DEFAULT 2.5,
    interval_days INTEGER DEFAULT 0,
    repetitions INTEGER DEFAULT 0,
    due_date TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, word, language)
)
"""

# NEW: one row per day the learner was active (for the streak)
CREATE_ACTIVITY_LOG_TABLE = """
CREATE TABLE IF NOT EXISTS activity_log (
    user_id INTEGER NOT NULL,
    day TEXT NOT NULL,
    xp INTEGER DEFAULT 0,
    PRIMARY KEY(user_id, day)
)
"""

# NEW: final book exam results
CREATE_EXAM_RESULTS_TABLE = """
CREATE TABLE IF NOT EXISTS exam_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    book_name TEXT NOT NULL,
    score INTEGER NOT NULL,
    total INTEGER NOT NULL,
    passed INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
"""

GET_TABLES = """
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
"""

ALL_TABLES = [
    CREATE_USERS_TABLE,
    CREATE_LESSONS_TABLE,
    CREATE_PROGRESS_TABLE,
    CREATE_READING_PROGRESS_TABLE,
    CREATE_OFFICIAL_BOOKS_TABLE,
    CREATE_BOOK_MEMORY_TABLE,
    CREATE_PAGE_MASTERY_TABLE,
    CREATE_VOCABULARY_TABLE,
    CREATE_ACTIVITY_LOG_TABLE,
    CREATE_EXAM_RESULTS_TABLE,
]


def init_db():
    """Creates every table. Safe to run every time the server starts."""
    from backend.database.connection import get_connection

    connection = get_connection()

    try:
        for statement in ALL_TABLES:
            connection.execute(statement)
        connection.commit()
    finally:
        connection.close()


if __name__ == "__main__":
    init_db()
    print("Database tables are ready.")