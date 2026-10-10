# backend/services/pdf_reader.py
from functools import lru_cache
from pathlib import Path

from docx import Document
from pypdf import PdfReader

from backend.config import USER_BOOKS_DIR
from backend.services.text_utils import paginate_text


@lru_cache(maxsize=8)
def _pdf_pages(path_text, modified):
    # Cached: the old code re-read the whole PDF on every single page request.
    reader = PdfReader(path_text)
    return tuple((page.extract_text() or "").strip() for page in reader.pages)


class PDFReader:

    def __init__(self):
        self.base_path = USER_BOOKS_DIR

    def get_file_path(self, file_name):
        path = self.base_path / Path(file_name).name

        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")

        if path.suffix.lower() != ".pdf":
            raise ValueError("Only PDF files are supported.")

        return path

    def extract_pages(self, path):
        """
        Returns the text of every page. This method was missing, so
        PassageService and BookExamService crashed on every call.
        Works for .pdf, .docx and .txt files.
        """
        path = Path(path)

        if not path.exists():
            path = self.base_path / path.name

        if not path.exists():
            raise FileNotFoundError(f"Book not found: {path.name}")

        suffix = path.suffix.lower()

        if suffix == ".pdf":
            return list(_pdf_pages(str(path), path.stat().st_mtime_ns))

        if suffix == ".docx":
            document = Document(str(path))
            text = "\n".join(
                p.text.strip() for p in document.paragraphs if p.text.strip()
            )
            return paginate_text(text)

        if suffix == ".txt":
            return paginate_text(
                path.read_text(encoding="utf-8"), path.parent.name
            )

        raise ValueError("Only PDF, DOCX and TXT files are supported.")

    def total_pages(self, file_name):
        return len(self.extract_pages(self.get_file_path(file_name)))

    def read_page(self, file_name, page_number):
        pages = self.extract_pages(self.get_file_path(file_name))

        if page_number < 1 or page_number > len(pages):
            raise ValueError(f"Page must be between 1 and {len(pages)}.")

        return pages[page_number - 1]

    def read_all_pages(self, file_name):
        return self.extract_pages(self.get_file_path(file_name))

    def read_entire_book(self, file_name):
        return "\n\n".join(self.read_all_pages(file_name))


if __name__ == "__main__":

    pdf = PDFReader()

    file_name = "lesson2.pdf"

    print(f"Total pages: {pdf.total_pages(file_name)}")
    print(pdf.read_page(file_name, 1))