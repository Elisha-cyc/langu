# backend/services/progress_service.py
from backend.database.progress_repository import (
    get_or_create_progress,
    complete_lesson,
    record_correct_answer,
    record_incorrect_answer,
    save_book_progress,
    load_book_progress
)


def get_user_progress(user_id):
    if user_id <= 0:
        raise ValueError("Invalid user ID.")

    return get_or_create_progress(user_id)


def lesson_completed(user_id, xp_amount=10):
    complete_lesson(user_id, xp_amount)


def correct_answer(user_id, xp_amount=5):
    record_correct_answer(user_id, xp_amount)


def incorrect_answer(user_id):
    record_incorrect_answer(user_id)


def save_reading_progress(user_id, book_name, page_number):
    if page_number < 1:
        raise ValueError("Page number must be at least 1.")

    save_book_progress(
        user_id,
        book_name,
        page_number
    )


def get_reading_progress(user_id, book_name):
    return load_book_progress(
        user_id,
        book_name
    )


if __name__ == "__main__":

    user_id = 1

    print("Current Progress")
    print(get_user_progress(user_id))

    print("\nSaving reading progress...")

    save_reading_progress(
        user_id,
        "lesson2.pdf",
        5
    )

    print(
        get_reading_progress(
            user_id,
            "lesson2.pdf"
        )
    )