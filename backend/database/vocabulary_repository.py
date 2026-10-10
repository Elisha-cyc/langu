# backend/database/vocabulary_repository.py   (NEW: flashcards with spaced repetition)
import sqlite3
from datetime import date, timedelta

from backend.database.connection import get_connection


def _connect():
    connection = get_connection()
    connection.row_factory = sqlite3.Row
    return connection


def add_word(user_id, word, meaning, language, source=""):
    """Returns True if the word was new, False if it was already saved."""
    word = (word or "").strip()[:200]

    if not word:
        return False

    connection = _connect()

    try:
        cursor = connection.execute(
            """
            INSERT OR IGNORE INTO vocabulary
            (user_id, word, meaning, language, source, due_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                user_id, word, (meaning or "").strip()[:400],
                language, (source or "")[:200], date.today().isoformat()
            )
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def list_words(user_id, language=None):
    connection = _connect()

    try:
        if language:
            rows = connection.execute(
                "SELECT * FROM vocabulary WHERE user_id = ? AND language = ? ORDER BY id DESC",
                (user_id, language)
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM vocabulary WHERE user_id = ? ORDER BY id DESC",
                (user_id,)
            ).fetchall()

        return [dict(r) for r in rows]
    finally:
        connection.close()


def due_cards(user_id, language=None, limit=20):
    connection = _connect()
    today = date.today().isoformat()

    try:
        sql = "SELECT * FROM vocabulary WHERE user_id = ? AND due_date <= ?"
        params = [user_id, today]

        if language:
            sql += " AND language = ?"
            params.append(language)

        sql += " ORDER BY due_date, id LIMIT ?"
        params.append(limit)

        return [dict(r) for r in connection.execute(sql, params).fetchall()]
    finally:
        connection.close()


def count_due(user_id, language=None):
    return len(due_cards(user_id, language, limit=500))


def count_words(user_id):
    connection = get_connection()

    try:
        cursor = connection.execute(
            "SELECT COUNT(*) FROM vocabulary WHERE user_id = ?", (user_id,)
        )
        return cursor.fetchone()[0]
    finally:
        connection.close()


def review_card(user_id, card_id, quality):
    """
    quality: 1 = Again, 4 = Good, 5 = Easy (simplified SM-2).
    Cards you forget come back tomorrow; cards you know come back later
    and later.
    """
    quality = max(0, min(5, int(quality)))

    connection = _connect()

    try:
        row = connection.execute(
            "SELECT * FROM vocabulary WHERE id = ? AND user_id = ?",
            (card_id, user_id)
        ).fetchone()

        if row is None:
            raise ValueError("Card not found.")

        ease = row["ease"] or 2.5
        repetitions = row["repetitions"] or 0
        interval = row["interval_days"] or 0

        if quality < 3:
            repetitions = 0
            interval = 1
        else:
            repetitions += 1

            if repetitions == 1:
                interval = 1
            elif repetitions == 2:
                interval = 3
            else:
                interval = max(1, round(interval * ease))

            ease = max(
                1.3,
                ease + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
            )

        due = (date.today() + timedelta(days=interval)).isoformat()

        connection.execute(
            """
            UPDATE vocabulary
            SET ease = ?, repetitions = ?, interval_days = ?, due_date = ?
            WHERE id = ? AND user_id = ?
            """,
            (ease, repetitions, interval, due, card_id, user_id)
        )
        connection.commit()

        return {"id": card_id, "interval_days": interval, "due_date": due}
    finally:
        connection.close()


def delete_word(user_id, card_id):
    connection = get_connection()

    try:
        connection.execute(
            "DELETE FROM vocabulary WHERE id = ? AND user_id = ?",
            (card_id, user_id)
        )
        connection.commit()
    finally:
        connection.close()