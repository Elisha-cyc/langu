# lesson_repository.py
from backend.database.connection import get_connection


# =====================================================
# OFFICIAL BOOKS
# =====================================================

def create_official_book(
    title,
    language,
    level,
    author,
    cover,
    file_name
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO official_books
        (title, language, level, author, cover, file_name)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (title, language, level, author, cover, file_name)
    )

    connection.commit()

    book_id = cursor.lastrowid

    connection.close()

    return book_id


def get_books_by_language(language):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM official_books
        WHERE language = ?
        ORDER BY level, title
        """,
        (language,)
    )

    books = cursor.fetchall()

    connection.close()

    return books


def get_all_official_books():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM official_books ORDER BY language, title"
    )

    books = cursor.fetchall()

    connection.close()

    return books


# =====================================================
# LESSONS
# =====================================================

def create_lesson(title, language, content, difficulty="Beginner"):

    if not title.strip():
        raise ValueError("Lesson title cannot be empty.")

    if not content.strip():
        raise ValueError("Lesson content cannot be empty.")

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO lessons
        (title, language, content, difficulty)
        VALUES (?, ?, ?, ?)
        """,
        (title, language, content, difficulty)
    )

    connection.commit()

    lesson_id = cursor.lastrowid

    connection.close()

    return lesson_id


def get_lesson(lesson_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM lessons WHERE id = ?",
        (lesson_id,)
    )

    lesson = cursor.fetchone()

    connection.close()

    return lesson


def get_all_lessons():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM lessons ORDER BY id DESC"
    )

    lessons = cursor.fetchall()

    connection.close()

    return lessons


def update_lesson(
    lesson_id,
    title,
    content,
    difficulty
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE lessons
        SET
            title = ?,
            content = ?,
            difficulty = ?
        WHERE id = ?
        """,
        (
            title,
            content,
            difficulty,
            lesson_id
        )
    )

    connection.commit()

    connection.close()


def delete_lesson(lesson_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM lessons WHERE id = ?",
        (lesson_id,)
    )

    connection.commit()

    connection.close()


if __name__ == "__main__":

    print("Official Books")
    print("----------------")

    for book in get_all_official_books():
        print(book)

    print("\nLessons")
    print("----------------")

    for lesson in get_all_lessons():
        print(lesson)