# page_mastery_repository.py
import sqlite3
from pathlib import Path

DATABASE = Path("data") / "language.db"


def connect():
    DATABASE.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATABASE)


def create_page_mastery_table():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS page_mastery(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        book_name TEXT NOT NULL,
        page_number INTEGER NOT NULL,
        score INTEGER DEFAULT 0,
        passed INTEGER DEFAULT 0,

        UNIQUE(user_id, book_name, page_number)
    )
    """)

    connection.commit()
    connection.close()


def save_page_score(
    user_id,
    book_name,
    page_number,
    score,
    passed
):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT OR REPLACE INTO page_mastery(
        user_id,
        book_name,
        page_number,
        score,
        passed
    )
    VALUES(?,?,?,?,?)
    """, (
        user_id,
        book_name,
        page_number,
        score,
        1 if passed else 0
    ))

    connection.commit()
    connection.close()


def get_page_status(
    user_id,
    book_name,
    page_number
):
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT score, passed
    FROM page_mastery
    WHERE user_id=?
    AND book_name=?
    AND page_number=?
    """, (
        user_id,
        book_name,
        page_number
    ))

    result = cursor.fetchone()

    connection.close()

    if result is None:
        return {
            "score": 0,
            "passed": False
        }

    return {
        "score": result[0],
        "passed": bool(result[1])
    }


def is_page_unlocked(
    user_id,
    book_name,
    page_number
):
    if page_number == 1:
        return True

    previous = get_page_status(
        user_id,
        book_name,
        page_number - 1
    )

    return previous["passed"]

def get_book_progress(user_id, book_name):

    connection = connect()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT COUNT(*)
    FROM page_mastery
    WHERE user_id=?
    AND book_name=?
    AND passed=1
    """, (user_id, book_name))

    completed = cursor.fetchone()[0]

    connection.close()

    return completed


def is_book_completed(
    user_id,
    book_name,
    total_pages
):

    completed = get_book_progress(
        user_id,
        book_name
    )

    return completed >= total_pages

if __name__ == "__main__":
    create_page_mastery_table()
    print("Page mastery table created.")