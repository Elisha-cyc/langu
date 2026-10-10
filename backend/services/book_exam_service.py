# backend/services/book_exam_service.py   (REAL exam: questions + grading)
import difflib
import random
import re
import threading
import time
import unicodedata
import uuid

from backend.ai.teacher import explain_text
from backend.config import EXAM_PASS_PERCENT, XP_EXAM_PASSED
from backend.database.progress_repository import (
    award_xp,
    has_passed_exam,
    save_exam_result
)
from backend.services.library_service import LibraryService
from backend.services.text_utils import book_digest

# Correct answers stay on the server so the browser can never read them.
_EXAMS = {}
_LOCK = threading.Lock()
EXAM_LIFETIME = 2 * 60 * 60


def _normalize(text):
    text = unicodedata.normalize("NFKC", str(text or "")).lower()
    text = re.sub(r"[^\w\s]", "", text)
    return re.sub(r"\s+", " ", text).strip()


class BookExamService:

    def __init__(self):
        self.library = LibraryService()

    def _clean_questions(self, raw):
        questions = []

        for item in raw if isinstance(raw, list) else []:
            if not isinstance(item, dict):
                continue

            text = str(item.get("question", "")).strip()
            answer = str(item.get("answer", "")).strip()
            kind = item.get("type")

            if not text or not answer:
                continue

            if kind == "multiple_choice":
                options = [str(o).strip() for o in item.get("options") or [] if str(o).strip()]
                match = next((o for o in options if _normalize(o) == _normalize(answer)), None)

                if len(options) < 2 or match is None:
                    continue

                random.shuffle(options)
                answer = match

            elif kind == "translation":
                options = []
            else:
                continue

            questions.append({
                "id": f"q{len(questions) + 1}",
                "type": kind,
                "question": text,
                "options": options,
                "answer": answer,
                "explanation": str(item.get("explanation", "")).strip()
            })

        return questions

    def generate_exam(
        self,
        file_name,
        target_language,
        learner_level,
        language=None,
        num_questions=10
    ):

        pages = self.library.get_pages(file_name)
        digest = book_digest(pages, 10000)

        if not digest.strip():
            raise ValueError("This book has no readable text to build an exam from.")

        result = explain_text(
            text=digest,
            target_language=target_language,
            learner_level=learner_level,
            mode="exam",
            learning_language=language or "Auto"
        )

        questions = self._clean_questions(result.get("questions"))

        if len(questions) < 3:
            raise RuntimeError("The AI could not build the exam. Please try again.")

        exam_id = uuid.uuid4().hex

        with _LOCK:
            now = time.time()

            for key in [k for k, v in _EXAMS.items() if now - v["created"] > EXAM_LIFETIME]:
                del _EXAMS[key]

            _EXAMS[exam_id] = {
                "questions": questions,
                "title": str(result.get("title") or file_name),
                "created": now
            }

        return {
            "exam_id": exam_id,
            "title": str(result.get("title") or file_name),
            "explained_in": result.get("explained_in", target_language),
            "questions": [
                {k: q[k] for k in ("id", "type", "question", "options")}
                for q in questions
            ]
        }

    def grade(self, exam_id, answers, user_id=None, book_name=None):

        with _LOCK:
            exam = _EXAMS.get(exam_id)

        if exam is None:
            raise FileNotFoundError("This exam expired. Please start a new one.")

        answers = answers if isinstance(answers, dict) else {}
        results, correct_count = [], 0

        for q in exam["questions"]:
            given = str(answers.get(q["id"], "")).strip()

            if q["type"] == "multiple_choice":
                correct = _normalize(given) == _normalize(q["answer"])
            else:
                ratio = difflib.SequenceMatcher(
                    None, _normalize(given), _normalize(q["answer"])
                ).ratio()
                correct = bool(given) and ratio >= 0.8

            correct_count += 1 if correct else 0

            results.append({
                "id": q["id"],
                "question": q["question"],
                "your_answer": given,
                "correct_answer": q["answer"],
                "correct": correct,
                "explanation": q["explanation"]
            })

        total = len(results)
        percent = round(correct_count / total * 100) if total else 0
        passed = percent >= EXAM_PASS_PERCENT
        xp_awarded = 0

        if user_id and book_name:
            first_pass = passed and not has_passed_exam(user_id, book_name)
            save_exam_result(user_id, book_name, correct_count, total, passed)

            if first_pass:
                award_xp(user_id, XP_EXAM_PASSED)
                xp_awarded = XP_EXAM_PASSED

        return {
            "score": correct_count,
            "total": total,
            "percent": percent,
            "passed": passed,
            "pass_percent": EXAM_PASS_PERCENT,
            "xp_awarded": xp_awarded,
            "results": results
        }