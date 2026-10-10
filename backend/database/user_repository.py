# backend/database/user_repository.py
from backend.database.connection import get_connection


def create_user(
    name,
    native_language,
    learning_language,
    learner_level
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users (
            name,
            native_language,
            learning_language,
            learner_level
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            name,
            native_language,
            learning_language,
            learner_level
        )
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


def get_user(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    return user


def update_user_profile(
    user_id,
    native_language,
    learning_language,
    learner_level
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE users
        SET
            native_language = ?,
            learning_language = ?,
            learner_level = ?
        WHERE id = ?
        """,
        (
            native_language,
            learning_language,
            learner_level,
            user_id
        )
    )

    connection.commit()
    connection.close()


def get_all_users():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users ORDER BY id"
    )

    users = cursor.fetchall()

    connection.close()

    return users


if __name__ == "__main__":

    user_id = create_user(
        "Elisha",
        "Twi",
        "Japanese",
        "intermediate"
    )

    print(get_user(user_id))