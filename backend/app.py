# backend/app.py
import os

# ---------- Prevent OpenBLAS memory errors ----------
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
os.environ["NUMEXPR_NUM_THREADS"] = "1"

import time
import uuid
from pathlib import Path

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.exceptions import HTTPException

from backend.config import (
    AUDIO_DIR, SCANS_DIR, DEBUG, NATIVE_LANGUAGES, LEARNING_LANGUAGES,
    LEVELS, PASS_SCORE, XP_PAGE_PASSED, XP_PAGE_SELF_ASSESSED,
    XP_FLASHCARD_REVIEW
)
from backend.database.models import init_db

# Creates every table (including the new ones) before anything uses them.
init_db()

from backend.ai.teacher import explain_text, result_to_text
from backend.database.page_mastery_repository import (
    save_page_score, get_page_status, get_book_progress, is_book_completed
)
from backend.database.progress_repository import (
    award_xp, complete_lesson, record_correct_answer,
    record_incorrect_answer, save_book_progress, load_book_progress
)
from backend.database import vocabulary_repository as vocab
from backend.lessons.exercises import ExerciseEngine
from backend.lessons.generator import LessonGenerator
from backend.routes.online_books import register_online_routes, list_native_books
from backend.services.audio_service import AudioService, VoiceUnavailable
from backend.services.book_exam_service import BookExamService
from backend.services.dashboard_service import DashboardService
from backend.services.library_service import LibraryService
from backend.services.ocr_service import OCRService
from backend.services.passage_service import PassageService
from backend.services.profile_service import ProfileService
from backend.services.pronunciation_service import PronunciationService

# =====================================================
# APP
# =====================================================

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
CORS(app)

from backend.security import install_security
install_security(app)

library_service = LibraryService()
dashboard_service = DashboardService()
passage_service = PassageService()
profile_service = ProfileService()
lesson_generator = LessonGenerator()
audio_service = AudioService()
ocr_service = OCRService()
pronunciation_service = PronunciationService()
book_exam_service = BookExamService()

register_online_routes(app, library_service, passage_service)


# =====================================================
# HELPERS
# =====================================================

def payload():
    return request.get_json(silent=True) or {}


def require(data, *keys):
    missing = [k for k in keys if data.get(k) in (None, "")]
    if missing:
        raise ValueError("Missing: " + ", ".join(missing))


def to_int(value, default=1):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def match(value, options, label):
    for option in options:
        if option.lower() == str(value).strip().lower():
            return option
    raise ValueError(f"Unsupported {label}: {value}")


def valid_book(name):
    return bool(name) and str(name).lower() not in ("undefined", "null", "none")


def cleanup_old_audio(hours=24):
    """Audio files were never deleted and piled up forever."""
    limit = time.time() - hours * 3600
    for pattern in ("*.mp3", "*.wav"):
        for file in AUDIO_DIR.glob(pattern):
            try:
                if file.stat().st_mtime < limit:
                    file.unlink()
            except OSError:
                pass


@app.errorhandler(Exception)
def handle_error(error):
    if isinstance(error, HTTPException):
        return jsonify({"error": error.description}), error.code

    message = str(error) or error.__class__.__name__

    if isinstance(error, FileNotFoundError) or "not found" in message.lower():
        status = 404
    elif isinstance(error, ValueError):
        status = 400
    elif isinstance(error, RuntimeError):
        status = 502
    else:
        status = 500
        app.logger.exception(error)

    return jsonify({"error": message}), status


# =====================================================
# HOME
# =====================================================

@app.get("/")
def home():
    return jsonify({"app": "Lingua AI", "version": "3.0.0", "status": "running"})


# =====================================================
# PROFILE
# =====================================================

@app.post("/profile")
def create_profile():
    data = payload()
    require(data, "name", "native_language", "learning_language", "learner_level")

    native = match(data["native_language"], NATIVE_LANGUAGES, "language")
    learning = match(data["learning_language"], LEARNING_LANGUAGES, "language")
    level = match(data["learner_level"], LEVELS, "level")

    if native == learning:
        raise ValueError("Choose two different languages.")

    profile = profile_service.create_profile(
        name=str(data["name"]).strip(),
        native_language=native,
        learning_language=learning,
        learner_level=level
    )

    return jsonify(profile), 201


@app.get("/profile/<int:user_id>")
def get_profile(user_id):
    return jsonify(profile_service.get_profile(user_id))


@app.put("/profile/<int:user_id>")
def update_profile(user_id):
    """Changing language / level used to create a brand new user."""
    data = payload()
    require(data, "native_language", "learning_language", "learner_level")

    native = match(data["native_language"], NATIVE_LANGUAGES, "language")
    learning = match(data["learning_language"], LEARNING_LANGUAGES, "language")
    level = match(data["learner_level"], LEVELS, "level")

    if native == learning:
        raise ValueError("Choose two different languages.")

    return jsonify(profile_service.update_profile(user_id, native, learning, level))


# =====================================================
# LIBRARY
# =====================================================

@app.get("/library")
def library():
    user_id = request.args.get("user_id", 1, type=int)
    profile = profile_service.get_profile(user_id)

    return jsonify({
        "official_books": library_service.get_official_books(user_id),
        "my_books": library_service.get_user_books(),
        "native_books": list_native_books(profile.get("learning_language", ""))
    })


@app.post("/library/import")
def import_book():
    book = request.files.get("book")

    if book is None:
        return jsonify({"error": "No book uploaded"}), 400

    return jsonify(library_service.import_book(book)), 201


# =====================================================
# DASHBOARD
# =====================================================

@app.get("/dashboard")
def dashboard():
    user_id = request.args.get("user_id", 1, type=int)
    return jsonify(dashboard_service.get_dashboard(user_id))


# =====================================================
# LESSONS
# =====================================================

@app.post("/lesson/generate")
def generate_lesson():
    data = payload()
    require(data, "passage", "language", "target_language", "learner_level", "title")

    return jsonify(lesson_generator.generate(
        passage=data["passage"],
        language=data["language"],
        target_language=data["target_language"],
        learner_level=data["learner_level"],
        title=data["title"],
        user_id=to_int(data.get("user_id")),
        page=to_int(data.get("page")),
    ))


@app.post("/lesson/curriculum")
def curriculum():
    data = payload()
    require(data, "language", "learner_level", "lesson_id", "target_language")

    return jsonify(lesson_generator.generate_from_curriculum(
        language=data["language"],
        learner_level=data["learner_level"],
        lesson_id=data["lesson_id"],
        target_language=data["target_language"],
        user_id=to_int(data.get("user_id")),
        page=to_int(data.get("page")),
        title=data.get("title")
    ))


@app.post("/lesson/exercises")
def lesson_exercises():
    data = payload()
    require(data, "passage")

    return jsonify(ExerciseEngine().generate(
        passage=data["passage"],
        target_language=data.get("target_language", "English"),
        learner_level=data.get("learner_level", "Beginner"),
        learning_language=data.get("language", "Auto")
    ))


# =====================================================
# BOOKS
# =====================================================

@app.post("/teach/page")
def teach_page():
    data = payload()
    require(data, "book")

    return jsonify(passage_service.teach_book_page(
        file_name=data["book"],
        page_number=to_int(data.get("page")),
        target_language=data.get("target_language", "English"),
        learner_level=data.get("learner_level", "Beginner"),
        language=data.get("language"),
        user_id=to_int(data.get("user_id"))
    ))


@app.post("/book/key-factors")
def key_factors():
    data = payload()
    require(data, "book")

    return jsonify(passage_service.book_key_factors(
        file_name=data["book"],
        target_language=data.get("target_language", "English"),
        learner_level=data.get("learner_level", "Beginner"),
        language=data.get("language")
    ))


@app.get("/book/resume")
def book_resume():
    user_id = request.args.get("user_id", 1, type=int)
    book = request.args.get("book_name", "")
    return jsonify({"page": load_book_progress(user_id, book)})


@app.post("/book/page")
def book_save_page():
    data = payload()
    require(data, "book_name", "page")

    if valid_book(data["book_name"]):
        save_book_progress(to_int(data.get("user_id")), data["book_name"], to_int(data["page"]))

    return jsonify({"saved": True})


@app.post("/book/progress")
def progress():
    data = payload()
    require(data, "user_id", "book_name", "total_pages")

    return jsonify({
        "completed_pages": get_book_progress(data["user_id"], data["book_name"]),
        "total_pages": data["total_pages"],
        "book_completed": is_book_completed(
            data["user_id"], data["book_name"], data["total_pages"]
        )
    })


# =====================================================
# FINAL BOOK EXAM
# =====================================================

@app.post("/book/exam")
def book_exam():
    data = payload()
    require(data, "book")

    return jsonify(book_exam_service.generate_exam(
        file_name=data["book"],
        target_language=data.get("target_language", "English"),
        learner_level=data.get("learner_level", "Beginner"),
        language=data.get("language")
    ))


@app.post("/book/exam/submit")
def book_exam_submit():
    data = payload()
    require(data, "exam_id")

    return jsonify(book_exam_service.grade(
        exam_id=data["exam_id"],
        answers=data.get("answers", {}),
        user_id=to_int(data.get("user_id")),
        book_name=data.get("book_name")
    ))


# =====================================================
# CAMERA SCAN
# =====================================================

@app.post("/scan")
def scan():
    image = request.files.get("image")

    if image is None:
        return jsonify({"error": "No image uploaded"}), 400

    extension = Path(image.filename or "").suffix.lower()

    if extension not in (".png", ".jpg", ".jpeg", ".webp"):
        return jsonify({"error": "Unsupported image format."}), 400

    language = request.form.get("language", "English")
    target_language = request.form.get("target_language", "English")
    learner_level = request.form.get("learner_level", "Beginner")
    user_id = to_int(request.form.get("user_id"))

    # A random file name: the uploaded name is never trusted.
    temp = SCANS_DIR / f"{uuid.uuid4().hex}{extension}"
    image.save(temp)

    try:
        text = ocr_service.scan_image(str(temp), language)
    finally:
        temp.unlink(missing_ok=True)

    lesson = lesson_generator.generate(
        passage=text, language=language, target_language=target_language,
        learner_level=learner_level, title="Camera Scan",
        user_id=user_id, page=1, remember=False
    )

    try:
        audio = audio_service.generate_audio(text=text[:3000], language=language)
    except VoiceUnavailable:
        audio = None

    return jsonify({"lesson": lesson, "audio": audio, "page_text": text})


@app.post("/text/summarize")
def summarize_text():
    data = payload()
    require(data, "text")

    mode = "summary" if data.get("mode", "summary") == "summary" else "key_points"

    result = explain_text(
        text=data["text"],
        target_language=data.get("target_language", "English"),
        learner_level=data.get("learner_level", "Beginner"),
        mode=mode,
        learning_language=data.get("language", "Auto")
    )

    return jsonify({
        "result": result_to_text(mode, result),
        "explained_in": result.get("explained_in")
    })


# =====================================================
# AUDIO
# =====================================================

@app.post("/audio/read")
def read_audio():
    data = payload()
    require(data, "text", "language")

    return jsonify({"audio": audio_service.generate_audio(
        text=data["text"], language=data["language"], calm=data.get("calm", False)
    )})


AUDIO_FOLDER = Path(AUDIO_DIR)


@app.get("/data/audio/<path:file_name>")
def serve_audio(file_name):
    return send_from_directory(AUDIO_FOLDER, file_name)


# =====================================================
# PRONUNCIATION + PAGE MASTERY
# =====================================================

@app.post("/pronunciation/analyze")
def pronunciation():
    audio = request.files.get("audio")

    if audio is None:
        return jsonify({"error": "Audio required"}), 400

    language = request.form.get("language", "")
    user_id = to_int(request.form.get("user_id"))
    book = request.form.get("book_name")
    page = to_int(request.form.get("page"))

    result = pronunciation_service.analyze(
        audio_file=audio,
        expected_text=request.form.get("expected", ""),
        language=language
    )

    score = result.get("score")
    passed = score is not None and score >= PASS_SCORE
    result["passed"] = passed
    result["xp_awarded"] = 0

    # Accuracy on the dashboard was always 0: attempts were never recorded.
    if score is not None:
        if passed:
            record_correct_answer(user_id, xp_amount=0)
        else:
            record_incorrect_answer(user_id)

        # A failed or error attempt used to save a NULL score.
        if valid_book(book):
            newly_passed = save_page_score(user_id, book, page, score, passed)

            if passed and newly_passed:
                complete_lesson(user_id, XP_PAGE_PASSED)
                result["xp_awarded"] = XP_PAGE_PASSED

    return jsonify(result)


@app.post("/page/complete")
def page_complete():
    """For languages without speaking scores (Twi): the learner confirms practice."""
    data = payload()
    require(data, "book_name", "page", "language")

    if pronunciation_service.supports(data["language"]):
        raise ValueError("Use the speaking practice for this language.")

    user_id = to_int(data.get("user_id"))
    newly = save_page_score(user_id, data["book_name"], to_int(data["page"]), 0, True)
    xp = 0

    if newly:
        complete_lesson(user_id, XP_PAGE_SELF_ASSESSED)
        xp = XP_PAGE_SELF_ASSESSED

    return jsonify({"passed": True, "xp_awarded": xp})


@app.post("/page/status")
def page_status():
    data = payload()
    require(data, "user_id", "book_name", "page")

    return jsonify(get_page_status(
        user_id=data["user_id"], book_name=data["book_name"], page_number=data["page"]
    ))


# =====================================================
# FLASHCARDS (spaced repetition)
# =====================================================

@app.post("/vocab/add")
def vocab_add():
    data = payload()
    require(data, "word", "language")

    added = vocab.add_word(
        to_int(data.get("user_id")), data["word"], data.get("meaning", ""),
        data["language"], data.get("source", "")
    )
    return jsonify({"added": added})


@app.get("/vocab/list")
def vocab_list():
    return jsonify({"words": vocab.list_words(
        request.args.get("user_id", 1, type=int), request.args.get("language") or None
    )})


@app.get("/vocab/due")
def vocab_due():
    user_id = request.args.get("user_id", 1, type=int)
    language = request.args.get("language") or None

    return jsonify({
        "cards": vocab.due_cards(user_id, language, request.args.get("limit", 20, type=int)),
        "due_total": vocab.count_due(user_id, language)
    })


@app.post("/vocab/review")
def vocab_review():
    data = payload()
    require(data, "card_id", "quality")
    user_id = to_int(data.get("user_id"))

    result = vocab.review_card(user_id, to_int(data["card_id"]), data["quality"])
    award_xp(user_id, XP_FLASHCARD_REVIEW)
    result["xp_awarded"] = XP_FLASHCARD_REVIEW

    return jsonify(result)


@app.delete("/vocab/<int:card_id>")
def vocab_delete(card_id):
    vocab.delete_word(request.args.get("user_id", 1, type=int), card_id)
    return jsonify({"deleted": True})


# =====================================================
# START SERVER
# =====================================================

def main():
    cleanup_old_audio()

    print("=" * 50)
    print("        LINGUA AI BACKEND SERVER")
    print("=" * 50)
    print("Home      : http://127.0.0.1:5000/")
    print("=" * 50)

    # debug=True with host 0.0.0.0 exposed Flask's debugger to your whole
    # network. It is now off unless you set FLASK_DEBUG=1 in .env.
    app.run(host="0.0.0.0", port=5000, debug=DEBUG)


if __name__ == "__main__":
    main()