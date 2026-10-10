# backend/services/library_service.py
import re
from pathlib import Path

from backend.config import USER_BOOKS_DIR, ONLINE_BOOKS_DIR
from backend.curriculum.engine import CurriculumEngine
from backend.database.user_repository import get_user
from backend.services.pdf_reader import PDFReader


class LibraryService:

    def __init__(self):

        self.curriculum = CurriculumEngine()
        self.pdf = PDFReader()

        # One folder for imported books. PDFReader used to look in a
        # different folder (data/library), so imported books could not be read.
        self.user_library = USER_BOOKS_DIR
        self.user_library.mkdir(parents=True, exist_ok=True)

        self.supported_formats = [".pdf", ".docx"]

    # ======================================
    # OFFICIAL LANGUAGE LIBRARY
    # ======================================

    def get_official_books(self, user_id):

        user = get_user(user_id)

        if not user:
            raise ValueError("User not found.")

        learning_language = user[3]
        learner_level = user[4]

        lessons = self.curriculum.get_lessons(
            learning_language,
            learner_level
        )

        # The passage is NOT sent in the list any more (it made /library huge).
        return [
            {
                "id": lesson["id"],
                "title": lesson["title"],
                "language": learning_language,
                "level": learner_level,
                "type": "official"
            }
            for lesson in lessons
        ]

    # ======================================
    # USER LIBRARY
    # ======================================

    def get_user_books(self):

        books = []

        for extension in self.supported_formats:

            for file in self.user_library.glob(f"*{extension}"):

                books.append({
                    "title": file.stem,
                    "file_name": file.name,
                    "type": extension.replace(".", "").upper(),
                    "size_kb": round(file.stat().st_size / 1024, 1)
                })

        books.sort(key=lambda book: book["title"].lower())

        return books

    @staticmethod
    def _safe_filename(name):
        # Keeps Japanese / Arabic names; only removes characters that are
        # dangerous in paths (the old code trusted the uploaded name).
        name = Path(str(name or "")).name
        return re.sub(r'[\\/:*?"<>|\x00-\x1f]', "_", name).strip() or "book"

    def import_book(self, uploaded_file, overwrite=False):

        if uploaded_file is None:
            raise ValueError("No file selected.")

        filename = self._safe_filename(uploaded_file.filename)
        extension = Path(filename).suffix.lower()

        if extension not in self.supported_formats:
            raise ValueError("Only PDF and DOCX files are supported.")

        destination = self.user_library / filename

        # Never silently replace someone's book with another one of the same name.
        if destination.exists() and not overwrite:
            stem, counter = Path(filename).stem, 1
            while destination.exists():
                destination = self.user_library / f"{stem}_{counter}{extension}"
                counter += 1

        uploaded_file.save(destination)

        return {
            "title": destination.stem,
            "file_name": destination.name,
            "type": extension.replace(".", "").upper(),
            "size_kb": round(destination.stat().st_size / 1024, 1)
        }

    def book_exists(self, book_name):
        return (self.user_library / Path(book_name).name).exists()

    def get_book_path(self, book_name):

        path = self.user_library / Path(book_name).name

        if not path.exists():
            raise FileNotFoundError(
                f"Book not found: {book_name}"
            )

        return path

    def delete_book(self, book_name):

        path = self.get_book_path(book_name)
        path.unlink()

        return True

    def total_user_books(self):

        return len(self.get_user_books())

    # ======================================
    # READING ANY BOOK BY NAME
    # ======================================

    def resolve_book_path(self, file_name):
        """
        "my_book.pdf"            -> an imported book
        "japanese/12_title.txt"  -> an online (Gutenberg) book
        One lookup for both, so every screen can open any book the same way.
        """

        name = str(file_name or "").replace("\\", "/")

        if "/" in name:
            root = ONLINE_BOOKS_DIR.resolve()
            path = (ONLINE_BOOKS_DIR / name).resolve()

            if root not in path.parents or not path.is_file():
                raise FileNotFoundError(
                    "Book not found. It may need to be added again."
                )

            return path

        return self.get_book_path(name)

    def get_pages(self, file_name):
        return self.pdf.extract_pages(self.resolve_book_path(file_name))


if __name__ == "__main__":

    library = LibraryService()

    print(library.get_official_books(1))
    print(library.get_user_books())