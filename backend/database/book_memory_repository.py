# backend/database/book_memory_repository.py
import sqlite3

DB = "data/language.db"


def connect():
    return sqlite3.connect(DB)


def create_book_memory_table():

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_memory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_title TEXT,
            language TEXT,
            current_page INTEGER,
            context TEXT
        )
    """)

    conn.commit()
    conn.close()


create_book_memory_table()

def save_memory(user_id, book_title, language, page, context):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM book_memory
        WHERE user_id=? AND book_title=?
    """, (user_id, book_title))

    cursor.execute("""
        INSERT INTO book_memory(
            user_id,
            book_title,
            language,
            current_page,
            context
        )
        VALUES(?,?,?,?,?)
    """, (
        user_id,
        book_title,
        language,
        page,
        context
    ))

    conn.commit()
    conn.close()


def load_memory(user_id, book_title):

    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT current_page, context
        FROM book_memory
        WHERE user_id=? AND book_title=?
    """, (
        user_id,
        book_title
    ))

    result = cursor.fetchone()

    conn.close()

    return result


if __name__ == "__main__":

    save_memory(
        1,
        "Japanese Beginner Book",
        "Japanese",
        5,
        '{"characters":["Sakura"],"vocabulary":["こんにちは"]}'
    )

    print(load_memory(
        1,
        "Japanese Beginner Book"
    ))