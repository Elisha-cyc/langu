# backend/services/passage_service.py
from backend.ai.detector import detect_language
from backend.ai.teacher import explain_text
from backend.database.progress_repository import (
    save_book_progress,
    load_book_progress
)
from backend.lessons.generator import LessonGenerator
from backend.services.lesson_detector import LessonDetector
from backend.services.library_service import LibraryService
from backend.services.text_utils import book_digest


class PassageService:

    def __init__(self):
        self.library = LibraryService()
        self.generator = LessonGenerator()
        self.lesson_detector = LessonDetector()

    # ==================================================
    # HELPERS
    # ==================================================

    def _resolve_language(self, language, passage):
        """
        The old code sent language="Auto", so the audio service had no voice
        for the sentence ("Auto" is not a language) and uploaded books had no
        sound. Use the learner's language, or detect it as a last resort.
        """

        if language and str(language).strip().lower() not in ("", "auto"):
            return language

        try:
            return detect_language(passage[:400])
        except Exception:
            return "Auto"

    # ==================================================
    # ANY BOOK PAGE (PDF, DOCX, imported online book)
    # ==================================================

    def teach_book_page(
        self,
        file_name,
        page_number,
        target_language="English",
        learner_level="Beginner",
        language=None,
        user_id=1
    ):

        pages = self.library.get_pages(file_name)
        total_pages = len(pages)

        # Validate BEFORE using the page number (the old code used it first).
        if page_number < 1 or page_number > total_pages:
            raise ValueError("Invalid page number.")

        passage = pages[page_number - 1].strip()

        if not passage:
            raise ValueError(
                "This page has no readable text (it may be a scanned image). "
                "Use Scan to read it."
            )

        language = self._resolve_language(language, passage)

        # The memory / context now lives in LessonGenerator, so the previous
        # page is no longer pasted into the passage and taught a second time.
        lesson = self.generator.generate(
            passage=passage,
            language=language,
            target_language=target_language,
            learner_level=learner_level,
            title=file_name,
            user_id=user_id,
            page=page_number,
            total_pages=total_pages
        )

        sections = self.lesson_detector.detect(pages)

        current = next(
            (
                section for section in sections
                if section["start_page"] <= page_number <= section["end_page"]
            ),
            sections[0]
        )

        lesson["lesson_id"] = current["lesson_id"]
        lesson["lesson_title"] = current["title"]
        lesson["lesson_start"] = current["start_page"]
        lesson["lesson_end"] = current["end_page"]

        return lesson

    # Old name, still used by older code.
    teach_pdf_page = teach_book_page

    # ==================================================
    # WHOLE BOOK KEY FACTORS
    # ==================================================

    def book_key_factors(
        self,
        file_name,
        target_language,
        learner_level,
        language=None
    ):

        pages = self.library.get_pages(file_name)

        # A whole book is far too big for one AI request: send a sample.
        digest = book_digest(pages)

        if not digest.strip():
            raise ValueError("This book has no readable text.")

        result = explain_text(
            text=digest,
            target_language=target_language,
            learner_level=learner_level,
            mode="key_factors",
            learning_language=language or "Auto"
        )

        return {
            "title": file_name,
            "key_factors": result,
            "explained_in": result.get("explained_in", target_language)
        }

    # ==================================================
    # BOOK PROGRESS
    # ==================================================

    def continue_book(
        self,
        user_id,
        file_name,
        target_language,
        learner_level,
        language=None
    ):

        return self.teach_book_page(
            file_name=file_name,
            page_number=load_book_progress(user_id, file_name),
            target_language=target_language,
            learner_level=learner_level,
            language=language,
            user_id=user_id
        )

    def finish_page(self, user_id, file_name, current_page):

        next_page = current_page + 1

        save_book_progress(user_id, file_name, next_page)

        return next_page