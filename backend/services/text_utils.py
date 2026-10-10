# backend/services/text_utils.py
import re

_HAN_KANA = r"\u3040-\u30ff\u3400-\u9fff\uf900-\ufaff\uff00-\uffef"

WORDS_PER_PAGE = 350
CHARS_PER_PAGE = 700
CHAR_PAGED_LANGUAGES = {"japanese", "chinese", "thai"}


def clean_passage(text):
    text = re.sub(r"[ \t\u00a0]+", " ", text or "")
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(rf"(?<=[{_HAN_KANA}])\s+(?=[{_HAN_KANA}])", "", text)
    return text.strip()


def split_sentences(text):
    parts = re.split(r"(?<=[。！？!?])\s*|(?<=\.)\s+", clean_passage(text))
    return [p.strip() for p in parts if p and p.strip()]


def _looks_char_paged(text):
    sample = (text or "")[:2000]
    if not sample:
        return False
    return len(re.findall(f"[{_HAN_KANA}]", sample)) > len(sample) * 0.3


def paginate_text(text, language=None):
    name = (language or "").strip().lower()

    if name in CHAR_PAGED_LANGUAGES:
        by_chars = True
    elif name and name != "auto":
        by_chars = False
    else:
        by_chars = _looks_char_paged(text)

    if by_chars:
        flat = re.sub(r"\s+", " ", text).strip()
        if name != "thai":
            flat = re.sub(rf"(?<=[{_HAN_KANA}])\s+(?=[{_HAN_KANA}])", "", flat)

        sentences = re.split(r"(?<=[。！？!?])", flat)
        pages, current = [], ""

        for sentence in sentences:
            if not sentence:
                continue
            if current and len(current) + len(sentence) > CHARS_PER_PAGE:
                pages.append(current)
                current = ""
            current += sentence
            while len(current) > CHARS_PER_PAGE * 2:
                pages.append(current[:CHARS_PER_PAGE])
                current = current[CHARS_PER_PAGE:]

        if current:
            pages.append(current)
        return pages or [""]

    words = (text or "").split()
    pages = [
        " ".join(words[i:i + WORDS_PER_PAGE])
        for i in range(0, len(words), WORDS_PER_PAGE)
    ]
    return pages or [""]


def book_digest(pages, max_chars=9000):
    """Evenly sampled copy of a whole book (a full book is too big for the AI)."""
    texts = [p.strip() for p in pages if p and p.strip()]
    if not texts:
        return ""

    if sum(len(t) for t in texts) <= max_chars:
        return "\n\n".join(texts)

    wanted = min(12, len(texts))
    step = (len(texts) - 1) / max(wanted - 1, 1)
    chosen = [texts[round(i * step)] for i in range(wanted)]
    per_page = max_chars // wanted

    return "\n\n".join(t[:per_page] for t in chosen)