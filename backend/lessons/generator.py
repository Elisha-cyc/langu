# backend/lessons/generator.py
import os
import json

from dotenv import load_dotenv
from groq import Groq

from backend.ai.teacher import explain_text
from backend.curriculum.engine import CurriculumEngine
from backend.database.book_memory_repository import (
    load_memory,
    save_memory
)

load_dotenv()

# Change the model in your .env file (GROQ_MODEL=...) if Groq retires this one.
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")

# Used only when the curriculum has no lesson for a language / level.
_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))
_PASSAGE_CACHE = {}


def _ai_lesson_passage(language, level, lesson_id, title):
    """Writes a short reading passage for a lesson the curriculum doesn't have.
    Cached so the same lesson keeps the same passage until the server restarts."""

    key = (language, level, str(lesson_id))

    if key in _PASSAGE_CACHE:
        return _PASSAGE_CACHE[key]

    prompt = (
        f'Write a short {level} level reading passage of 4 to 6 simple '
        f'sentences in {language} for a language lesson titled "{title}" '
        f'(lesson {lesson_id}). Use only {language}. '
        f'Return ONLY the passage text, nothing else.'
    )

    reply = _groq.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}]
    )

    passage = reply.choices[0].message.content.strip()
    _PASSAGE_CACHE[key] = passage
    return passage


def _join_text(teachings, key):
    return " ".join(
        t[key] for t in teachings
        if isinstance(t.get(key), str) and t[key].strip()
    )


def _join_lists(teachings, key):
    items = []
    for t in teachings:
        if isinstance(t.get(key), list):
            items.extend(t[key])
    return items


class LessonGenerator:

    def __init__(self):
        self.curriculum = CurriculumEngine()

    # ==========================================
    # Generate lesson from any passage
    # ==========================================

    def generate(
        self,
        passage,
        language,
        target_language="English",
        learner_level="Beginner",
        title="AI Lesson",
        difficulty="Beginner",
        user_id=1,
        page=1,
        total_pages=1
    ):

        memory = load_memory(user_id, title)

        previous_context = ""

        if memory:
            previous_context = memory[1]

        ai_input = f"""
Previous Context:
{previous_context}

Current Page:
{passage}
"""

        teaching = explain_text(
            text=ai_input,
            target_language=target_language,
            learner_level=learner_level,
            mode="teach"
        )

        # AI returns one teaching object or a list of sentence steps
        if isinstance(teaching, dict) and "steps" in teaching:
            steps = teaching["steps"]
        else:
            # fallback for older AI responses
            steps = [{
                "sentence": passage,
                "teaching": teaching
            }]

        # Page-level teaching (used by the Summary screen), built from
        # every step instead of only the first one.
        step_teachings = [
            s["teaching"] for s in steps
            if isinstance(s, dict) and isinstance(s.get("teaching"), dict)
        ]

        lesson_content = {
            "passage": passage,
            "steps": steps,
            "teaching": {
                "translation": _join_text(step_teachings, "translation"),
                "vocabulary": _join_lists(step_teachings, "vocabulary"),
                "grammar": _join_text(step_teachings, "grammar"),
                "pronunciation": _join_text(step_teachings, "pronunciation"),
                "examples": _join_lists(step_teachings, "examples"),
                "practice": _join_text(step_teachings, "practice")
            }
        }

        new_memory = json.dumps({
            "last_page": page,
            "passage": passage
        })

        save_memory(
            user_id,
            title,
            language,
            page,
            new_memory
        )

        return {
            "title": title,
            "language": language,
            "page": page,
            "total_pages": total_pages,
            "content": lesson_content
        }

    # ==========================================
    # Official curriculum
    # ==========================================

    def generate_from_curriculum(
        self,
        language,
        learner_level,
        lesson_id,
        target_language,
        user_id=1,
        page=1,
        title=None
    ):

        try:
            lesson = self.curriculum.get_lesson(
                language,
                learner_level,
                lesson_id
            )
        except Exception:
            lesson = None

        if lesson:
            passage = lesson["passage"]
            lesson_title = lesson["title"]
        else:
            # Curriculum has nothing for this language / level: let the AI
            # write the passage so every language still gets a lesson.
            lesson_title = title or f"Lesson {lesson_id}"
            passage = _ai_lesson_passage(
                language,
                learner_level,
                lesson_id,
                lesson_title
            )

        return self.generate(
            passage=passage,
            language=language,
            target_language=target_language,
            learner_level=learner_level,
            title=lesson_title,
            difficulty=learner_level,
            user_id=user_id,
            page=page,
            total_pages=1
        )


if __name__ == "__main__":

    generator = LessonGenerator()

    lesson = generator.generate_from_curriculum(
        language="Japanese",
        learner_level="Beginner",
        lesson_id=1,
        target_language="English"
    )

    print(json.dumps(lesson, ensure_ascii=False, indent=2))