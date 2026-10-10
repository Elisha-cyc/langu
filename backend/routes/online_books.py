# backend/routes/online_books.py   (the Gutenberg + native-book code moved out of app.py)
import hashlib
import json
import re
import time
import unicodedata
from pathlib import Path

import requests
from flask import jsonify, request
from requests.adapters import HTTPAdapter, Retry
from werkzeug.datastructures import FileStorage

from backend.config import NATIVE_BOOKS_DIR, ONLINE_BOOKS_DIR
from backend.services.text_utils import paginate_text

SEARCH_CACHE_DIR = ONLINE_BOOKS_DIR / "_cache"
SEARCH_CACHE_DIR.mkdir(parents=True, exist_ok=True)
SEARCH_CACHE_TTL = 6 * 60 * 60

GUTENDEX_LANGUAGE_CODES = {
    "twi": "tw", "chinese": "zh", "french": "fr", "dutch": "nl",
    "german": "de", "hebrew": "he", "portuguese": "pt", "spanish": "es",
    "turkish": "tr", "vietnamese": "vi", "japanese": "ja", "swedish": "sv",
    "hindi": "hi", "arabic": "ar", "greek": "el", "italian": "it",
    "polish": "pl", "korean": "ko", "russian": "ru", "thai": "th",
    "english": "en",
}

HTTP_TIMEOUT = (6, 15)

_session = requests.Session()
_retries = Retry(total=1, backoff_factor=1, status_forcelist=[502, 503, 504],
                 allowed_methods=["GET"])
_session.mount("https://", HTTPAdapter(max_retries=_retries))
_session.mount("http://", HTTPAdapter(max_retries=_retries))


def _network_error(e):
    if isinstance(e, requests.exceptions.Timeout):
        return ("The online library is taking too long to respond. "
                "Please try again in a moment."), 504
    if isinstance(e, requests.exceptions.ConnectionError):
        return ("Couldn't connect to the online library. "
                "Please check your internet connection."), 502
    return f"Couldn't reach the online library: {e}", 502


def _safe_name(text):
    text = unicodedata.normalize("NFKD", str(text))
    text = re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")
    return text[:60] or "book"


def _clean_gutenberg(raw_bytes):
    try:
        text = raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw_bytes.decode("latin-1", errors="replace")

    start = re.search(
        r"\*\*\* ?START OF (THE|THIS) PROJECT GUTENBERG EBOOK.*?\*\*\*",
        text, re.I | re.S)
    if start:
        text = text[start.end():]

    end = re.search(r"\*\*\* ?END OF (THE|THIS) PROJECT GUTENBERG EBOOK", text, re.I)
    if end:
        text = text[:end.start()]

    return text.strip()


def _cache_file(code, page, query):
    key = hashlib.md5(query.strip().lower().encode("utf-8")).hexdigest()[:10]
    return SEARCH_CACHE_DIR / f"{code}_{page}_{key}.json"


def _read_cache(path):
    try:
        return json.loads(path.read_text(encoding="utf-8")), path.stat().st_mtime
    except Exception:
        return None, 0


def _download_book_text(gutenberg_id):
    direct_urls = [
        f"https://www.gutenberg.org/cache/epub/{gutenberg_id}/pg{gutenberg_id}.txt",
        f"https://www.gutenberg.org/ebooks/{gutenberg_id}.txt.utf-8",
    ]

    for url in direct_urls:
        try:
            r = _session.get(url, timeout=HTTP_TIMEOUT)
            r.raise_for_status()
            if r.content:
                return r.content
        except requests.RequestException:
            continue

    info = _session.get(f"https://gutendex.com/books/{gutenberg_id}", timeout=HTTP_TIMEOUT)
    info.raise_for_status()

    text_url = next(
        (url for key, url in info.json().get("formats", {}).items()
         if key.startswith("text/plain") and not url.endswith(".zip")),
        None)

    if not text_url:
        raise ValueError("No readable text version of this book.")

    r = _session.get(text_url, timeout=HTTP_TIMEOUT)
    r.raise_for_status()
    return r.content


def list_native_books(language):
    folder = NATIVE_BOOKS_DIR / Path(str(language)).name.lower()

    if not language or not folder.is_dir():
        return []

    books = []

    for f in sorted(folder.iterdir()):
        if f.suffix.lower() in (".pdf", ".docx"):
            books.append({
                "title": f.stem.replace("_", " ").replace("-", " ").title(),
                "file_name": f.name,
                "type": f.suffix[1:].upper(),
                "size_kb": round(f.stat().st_size / 1024),
                "language": language
            })

    return books


def register_online_routes(app, library_service, passage_service):

    @app.post("/library/native/open")
    def open_native_book():
        data = request.get_json(silent=True) or {}
        language = Path(str(data.get("language", ""))).name.lower()
        name = Path(str(data.get("file_name", ""))).name
        path = NATIVE_BOOKS_DIR / language / name

        if not path.is_file():
            return jsonify({"error": "Book not found."}), 404

        with open(path, "rb") as handle:
            book = library_service.import_book(
                FileStorage(stream=handle, filename=name), overwrite=True
            )

        return jsonify(book)

    @app.get("/library/online/search")
    def search_online_books():
        language = request.args.get("language", "")
        query = request.args.get("query", "")
        page = request.args.get("page", 1, type=int)

        code = GUTENDEX_LANGUAGE_CODES.get(language.strip().lower())

        if not code:
            return jsonify({
                "results": [], "has_more": False,
                "note": f"No online source configured for {language}."
            })

        cache_path = _cache_file(code, page, query)
        cached, cached_at = _read_cache(cache_path)

        if cached and time.time() - cached_at < SEARCH_CACHE_TTL:
            return jsonify(cached)

        params = {"languages": code, "page": page}
        if query:
            params["search"] = query

        try:
            response = _session.get("https://gutendex.com/books", params=params,
                                    timeout=HTTP_TIMEOUT)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            if cached:
                return jsonify({**cached, "note": "The online library is unreachable "
                                "right now, so these are saved results."})
            message, status = _network_error(e)
            return jsonify({"error": message}), status

        results = []

        for book in data.get("results", []):
            formats = book.get("formats", {})
            text_url = next(
                (url for key, url in formats.items()
                 if key.startswith("text/plain") and not url.endswith(".zip")),
                None)

            if not text_url:
                continue

            results.append({
                "gutenberg_id": book["id"],
                "title": book.get("title", "Untitled"),
                "author": ", ".join(p["name"] for p in book.get("authors", []))
                          or "Unknown author",
                "language": language,
            })

        payload = {"results": results, "has_more": bool(data.get("next"))}

        try:
            cache_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

        return jsonify(payload)

    @app.post("/library/online/add")
    def add_online_book():
        data = request.get_json(silent=True) or {}
        language = data.get("language", "")
        gutenberg_id = data.get("gutenberg_id")
        title = data.get("title", "Untitled")
        author = data.get("author", "")

        if not gutenberg_id:
            return jsonify({"error": "gutenberg_id is required."}), 400

        folder_name = _safe_name(language).lower()
        folder = ONLINE_BOOKS_DIR / folder_name
        folder.mkdir(parents=True, exist_ok=True)

        file_name = f"{int(gutenberg_id)}_{_safe_name(title)}.txt"
        path = folder / file_name

        if not path.exists():
            try:
                cleaned = _clean_gutenberg(_download_book_text(gutenberg_id))

                if not cleaned:
                    return jsonify({"error": "This book has no readable text."}), 502

                path.write_text(cleaned, encoding="utf-8")

            except ValueError as e:
                return jsonify({"error": str(e)}), 502
            except Exception as e:
                message, status = _network_error(e)
                return jsonify({"error": message}), status

        text = path.read_text(encoding="utf-8")
        total_pages = len(paginate_text(text, folder_name))

        try:
            path.with_suffix(".json").write_text(json.dumps({
                "gutenberg_id": int(gutenberg_id), "title": title,
                "author": author, "language": language, "total_pages": total_pages,
            }, ensure_ascii=False), encoding="utf-8")
        except Exception:
            pass

        return jsonify({
            "title": title,
            "file_name": f"{folder_name}/{file_name}",
            "type": "Online Book",
            "language": language,
            "total_pages": total_pages,
            "source": "gutenberg"
        })

    @app.get("/library/online/saved")
    def saved_online_books():
        language = request.args.get("language", "")
        folder = ONLINE_BOOKS_DIR / _safe_name(language).lower()

        if not language or not folder.is_dir():
            return jsonify({"results": []})

        results = []

        for txt in sorted(folder.glob("*.txt"), key=lambda p: p.stat().st_mtime, reverse=True):
            meta = None
            meta_path = txt.with_suffix(".json")

            if meta_path.is_file():
                try:
                    meta = json.loads(meta_path.read_text(encoding="utf-8"))
                except Exception:
                    meta = None

            if not meta:
                book_id, _, rest = txt.stem.partition("_")
                if not book_id.isdigit():
                    continue
                meta = {"gutenberg_id": int(book_id),
                        "title": rest.replace("_", " ") or "Untitled", "author": ""}

            results.append({
                "gutenberg_id": meta["gutenberg_id"],
                "title": meta.get("title", "Untitled"),
                "author": meta.get("author", ""),
                "language": language,
                "size_kb": round(txt.stat().st_size / 1024),
            })

        return jsonify({"results": results})

    @app.post("/teach/online-page")
    def teach_online_page():
        # Kept so older app versions keep working: it is the same lesson as /teach/page.
        data = request.get_json(silent=True) or {}

        lesson = passage_service.teach_book_page(
            file_name=data["book"],
            page_number=int(data.get("page", 1)),
            target_language=data.get("target_language", "English"),
            learner_level=data.get("learner_level", "Beginner"),
            language=data.get("language"),
            user_id=int(data.get("user_id", 1))
        )

        return jsonify(lesson)