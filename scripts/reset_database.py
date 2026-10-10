from backend.database.connection import get_connection

from backend.database.models import (
    CREATE_USERS_TABLE,
    CREATE_LESSONS_TABLE,
    CREATE_PROGRESS_TABLE,
    CREATE_OFFICIAL_BOOKS_TABLE,
)

from scripts.seed_data import seed_books


def reset_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS progress")
    cursor.execute("DROP TABLE IF EXISTS lessons")
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS official_books")

    cursor.execute(CREATE_USERS_TABLE)
    cursor.execute(CREATE_LESSONS_TABLE)
    cursor.execute(CREATE_PROGRESS_TABLE)
    cursor.execute(CREATE_OFFICIAL_BOOKS_TABLE)

    connection.commit()
    connection.close()

    print("=" * 40)
    print("Database recreated successfully")
    print("=" * 40)

    seed_books()


if __name__ == "__main__":
    reset_database()