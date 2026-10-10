# backend/services/book_memory_service.py
from pathlib import Path
import json


class BookMemoryService:

    def __init__(self):
        self.folder = Path("data") / "memory"
        self.folder.mkdir(parents=True, exist_ok=True)

    def _path(self, book_name):
        return self.folder / f"{book_name}.json"

    # ==========================================
    # Load memory
    # ==========================================

    def load(self, book_name):
        path = self._path(book_name)

        if not path.exists():
            return []

        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    # ==========================================
    # Save one page
    # ==========================================

    def save_page(self, book_name, page, text):
        memory = self.load(book_name)

        # Remove duplicate page if it already exists
        memory = [m for m in memory if m["page"] != page]

        # Always save as plain string
        memory.append({
            "page": page,
            "text": str(text)
        })

        memory.sort(key=lambda x: x["page"])

        with open(self._path(book_name), "w", encoding="utf-8") as file:
            json.dump(memory, file, ensure_ascii=False, indent=2)

    # ==========================================
    # Get previous pages
    # ==========================================

    def previous_context(self, book_name, current_page):
        memory = self.load(book_name)

        previous = []

        for item in memory:

            if item["page"] >= current_page:
                continue

            text = item.get("text", "")

            # Safety: old memory files may contain dictionaries
            if isinstance(text, dict):
                text = text.get("passage", "")

            previous.append(str(text))

        return "\n".join(previous[-5:])

    # ==========================================
    # Clear memory
    # ==========================================

    def clear(self, book_name):
        path = self._path(book_name)

        if path.exists():
            path.unlink()