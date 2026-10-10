# backend/services/lesson_service.py
from backend.database.lesson_repository import create_lesson
from backend.services.progress_service import lesson_completed

def create_and_complete_lesson(
  user_id,
  title,
  language,
  content
):
  lesson_id = create_lesson(
    title,
    language,
    content
  )

  lesson_completed(user_id)

  return lesson_id

if __name__ == "__main__":
    lesson_id = create_and_complete_lesson(
        1,
        "Chinese Introduction",
        "Chinese",
        "我叫李明。我住在北京。"
    )

    print("Lesson created with ID:", lesson_id)