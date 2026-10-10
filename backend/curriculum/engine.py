# engine.py
from importlib import import_module


class CurriculumEngine:

    def get_lessons(self, language, level):

        language = language.lower().replace(" ", "_")
        level = level.lower()

        module = import_module(
            f"backend.curriculum.{language}.{level}"
        )

        return getattr(module, "LESSONS", [])

    def get_lesson(self, language, level, lesson_id):

        lessons = self.get_lessons(language, level)

        for lesson in lessons:

            if lesson["id"] == lesson_id:
                return lesson

        return None