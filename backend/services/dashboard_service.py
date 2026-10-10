# backend/services/dashboard_service.py
from backend.database.progress_repository import (
    get_or_create_progress,
    get_streak
)
from backend.database.user_repository import get_user
from backend.database.vocabulary_repository import count_due, count_words
from backend.services.library_service import LibraryService


class DashboardService:

    def __init__(self):
        self.library = LibraryService()

    def get_dashboard(self, user_id):

        user = get_user(user_id)

        if not user:
            raise ValueError("User not found.")

        # progress columns: id, user_id, lessons_completed, correct, incorrect, xp
        stats = get_or_create_progress(user_id)

        lessons_completed = stats[2]
        correct_answers = stats[3]
        incorrect_answers = stats[4]
        xp = stats[5]

        total_answers = correct_answers + incorrect_answers
        accuracy = (
            0 if total_answers == 0
            else round((correct_answers / total_answers) * 100)
        )

        total_books = (
            len(self.library.get_official_books(user_id))
            + len(self.library.get_user_books())
        )

        return {
            "user": {
                "id": user[0],
                "name": user[1],
                "native_language": user[2],
                "learning_language": user[3],
                "learner_level": user[4],
                "xp": xp,
                "level": xp // 100 + 1
            },
            "library": {
                "total_books": total_books
            },
            "progress": {
                "lessons_completed": lessons_completed,
                "correct_answers": correct_answers,
                "incorrect_answers": incorrect_answers,
                "xp": xp,
                "accuracy": accuracy
            },
            "streak": get_streak(user_id),
            "due_cards": count_due(user_id, user[3]),
            "words_saved": count_words(user_id)
        }


if __name__ == "__main__":
    print(DashboardService().get_dashboard(1))