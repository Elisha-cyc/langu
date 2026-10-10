# curriculum_cache.py
import json
from pathlib import Path

# Curriculum lessons are static and identical for every learner at a given
# level -- only the target_language changes what the AI needs to produce
# (translations are INTO that language). So the cache key is
# (language, level, lesson_id, target_language), and once any learner
# triggers generation for a given combination, every other learner with the
# same combination is served from disk instead of hitting the AI again.
#
# NOTE: this is a simple JSON-file cache, with no file locking -- fine at
# small/medium scale, but if two requests for the *same* uncached lesson
# land at the same instant, both could miss the cache and generate/write
# concurrently (last write wins, no corruption, just a wasted duplicate
# AI call). If you already have a proper database (e.g. whatever
# book_memory_repository.py uses under the hood), a table there would be a
# more robust home for this -- happy to move it if you send that file.

CACHE_DIR = Path("data") / "curriculum_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


def _cache_path(language, level):
    language = language.lower().replace(" ", "_")
    level = level.lower()
    return CACHE_DIR / f"{language}_{level}.json"


def _cache_key(lesson_id, target_language):
    return f"{lesson_id}_{target_language}"


def _load_cache_file(language, level):
    path = _cache_path(language, level)

    if not path.exists():
        return {}

    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        # Corrupt/unreadable cache file -- treat as empty rather than
        # crashing lesson generation over a cache problem.
        return {}


def get_cached_lesson(language, level, lesson_id, target_language):
    """
    Returns the previously generated lesson dict for this
    (language, level, lesson_id, target_language) combination, or None if
    it hasn't been generated yet.
    """
    cache = _load_cache_file(language, level)
    return cache.get(_cache_key(lesson_id, target_language))


def save_cached_lesson(language, level, lesson_id, target_language, lesson_data):
    path = _cache_path(language, level)
    cache = _load_cache_file(language, level)
    cache[_cache_key(lesson_id, target_language)] = lesson_data

    with open(path, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def clear_cached_lesson(language, level, lesson_id, target_language):
    """
    Manual escape hatch to force one lesson to regenerate next time it's
    requested -- e.g. after improving the AI prompt and wanting existing
    cached lessons to pick up the change.
    """
    path = _cache_path(language, level)
    cache = _load_cache_file(language, level)
    key = _cache_key(lesson_id, target_language)

    if key in cache:
        del cache[key]
        with open(path, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
