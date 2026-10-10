# backend/database/progress_repository.py   (REPLACES the batch-1 version)
from datetime import date, timedelta

from backend.database.connection import get_connection


def _ensure_progress(cursor, user_id):
    cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))

    if cursor.fetchone() is None:
        raise ValueError("User not found.")

    cursor.execute(
        "INSERT OR IGNORE INTO progress (user_id) VALUES (?)",
        (user_id,)
    )


def _log_activity(cursor, user_id, xp=0):
    """Marks today as an active day (used for the streak)."""
    cursor.execute(
        """
        INSERT INTO activity_log (user_id, day, xp) VALUES (?, ?, ?)
        ON CONFLICT(user_id, day) DO UPDATE SET xp = xp + excluded.xp
        """,
        (user_id, date.today().isoformat(), xp)
    )


def _add_xp(cursor, user_id, amount):
    if amount:
        cursor.execute(
            "UPDATE progress SET xp = xp + ? WHERE user_id = ?",
            (amount, user_id)
        )
        cursor.execute(
            "UPDATE users SET xp = xp + ? WHERE id = ?",
            (amount, user_id)
        )

    _log_activity(cursor, user_id, amount or 0)


def create_progress(user_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        _ensure_progress(cursor, user_id)
        cursor.execute("SELECT id FROM progress WHERE user_id = ?", (user_id,))
        progress_id = cursor.fetchone()[0]
        connection.commit()
        return progress_id
    finally:
        connection.close()


def get_progress(user_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT id, user_id, lessons_completed, correct_answers,
                   incorrect_answers, xp
            FROM progress
            WHERE user_id = ?
            """,
            (user_id,)
        )
        return cursor.fetchone()
    finally:
        connection.close()


def get_or_create_progress(user_id):
    progress = get_progress(user_id)

    if progress:
        return progress

    create_progress(user_id)
    return get_progress(user_id)


def complete_lesson(user_id, xp_amount=10):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        _ensure_progress(cursor, user_id)
        cursor.execute(
            "UPDATE progress SET lessons_completed = lessons_completed + 1 WHERE user_id = ?",
            (user_id,)
        )
        _add_xp(cursor, user_id, xp_amount)
        connection.commit()
    finally:
        connection.close()


def record_correct_answer(user_id, xp_amount=5):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        _ensure_progress(cursor, user_id)
        cursor.execute(
            "UPDATE progress SET correct_answers = correct_answers + 1 WHERE user_id = ?",
            (user_id,)
        )
        _add_xp(cursor, user_id, xp_amount)
        connection.commit()
    finally:
        connection.close()


def record_incorrect_answer(user_id):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        _ensure_progress(cursor, user_id)
        cursor.execute(
            "UPDATE progress SET incorrect_answers = incorrect_answers + 1 WHERE user_id = ?",
            (user_id,)
        )
        _log_activity(cursor, user_id, 0)
        connection.commit()
    finally:
        connection.close()


def award_xp(user_id, amount):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        _ensure_progress(cursor, user_id)
        _add_xp(cursor, user_id, amount)
        connection.commit()
    finally:
        connection.close()


def get_streak(user_id):
    """Number of days in a row the learner was active (today or yesterday counts)."""
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT day FROM activity_log WHERE user_id = ? ORDER BY day DESC LIMIT 400",
            (user_id,)
        )
        days = {row[0] for row in cursor.fetchall()}
    finally:
        connection.close()

    today = date.today()

    if today.isoformat() in days:
        cursor_day = today
    elif (today - timedelta(days=1)).isoformat() in days:
        cursor_day = today - timedelta(days=1)
    else:
        return 0

    streak = 0

    while cursor_day.isoformat() in days:
        streak += 1
        cursor_day -= timedelta(days=1)

    return streak


def save_book_progress(user_id, book_name, page_number):
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT OR REPLACE INTO reading_progress
            (user_id, book_name, current_page)
            VALUES (?, ?, ?)
            """,
            (user_id, book_name, page_number)
        )
        connection.commit()
    finally:
        connection.close()


def load_book_progress(user_id, book_name):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT current_page FROM reading_progress WHERE user_id = ? AND book_name = ?",
            (user_id, book_name)
        )
        result = cursor.fetchone()
    finally:
        connection.close()

    return result[0] if result else 1


def save_exam_result(user_id, book_name, score, total, passed):
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO exam_results (user_id, book_name, score, total, passed)
            VALUES (?, ?, ?, ?, ?)
            """,
            (user_id, book_name, score, total, 1 if passed else 0)
        )
        connection.commit()
    finally:
        connection.close()


def has_passed_exam(user_id, book_name):
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT 1 FROM exam_results WHERE user_id = ? AND book_name = ? AND passed = 1 LIMIT 1",
            (user_id, book_name)
        )
        return cursor.fetchone() is not None
    finally:
        connection.close()


if __name__ == "__main__":
    print(get_or_create_progress(1))