# book_progress_repository.py
import sqlite3

DB = "data/language.db"

def unlock_page(user_id, book_name, page, score):

    connection = sqlite3.connect(DB)
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO book_progress
    (user_id, book_name, page, unlocked, best_score)

    VALUES (?, ?, ?, 1, ?)

    ON CONFLICT(user_id, book_name, page)

    DO UPDATE SET

    unlocked=1,
    best_score=max(best_score, excluded.best_score)
    """, (user_id, book_name, page, score))

    connection.commit()
    connection.close()


def is_page_unlocked(user_id, book_name, page):

    if page == 1:
        return True

    connection = sqlite3.connect(DB)
    cursor = connection.cursor()

    cursor.execute("""
    SELECT unlocked

    FROM book_progress

    WHERE user_id=?
    AND book_name=?
    AND page=?
    """, (user_id, book_name, page))

    row = cursor.fetchone()

    connection.close()

    return bool(row and row[0] == 1)