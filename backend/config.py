# backend/config.py
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

AUDIO_DIR = DATA_DIR / "audio"
USER_AUDIO_DIR = AUDIO_DIR / "user"
USER_BOOKS_DIR = DATA_DIR / "user_books"
SCANS_DIR = DATA_DIR / "scans"
NATIVE_BOOKS_DIR = DATA_DIR / "native_books"
ONLINE_BOOKS_DIR = DATA_DIR / "online_books"

for _folder in (AUDIO_DIR, USER_AUDIO_DIR, USER_BOOKS_DIR, SCANS_DIR,
                NATIVE_BOOKS_DIR, ONLINE_BOOKS_DIR):
    _folder.mkdir(parents=True, exist_ok=True)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
DEBUG = os.getenv("FLASK_DEBUG", "0") == "1"

LEARNING_LANGUAGES = [
    "Arabic", "Chinese", "Dutch", "French", "German", "Greek", "Hebrew",
    "Hindi", "Italian", "Japanese", "Korean", "Polish", "Portuguese",
    "Russian", "Spanish", "Swedish", "Thai", "Turkish", "Twi", "Vietnamese",
]
NATIVE_LANGUAGES = ["English"] + LEARNING_LANGUAGES
LEVELS = ["Beginner", "Intermediate", "Advanced"]

PASS_SCORE = 80
EXAM_PASS_PERCENT = 70
XP_PAGE_PASSED = 25
XP_PAGE_SELF_ASSESSED = 10
XP_EXAM_PASSED = 50
XP_FLASHCARD_REVIEW = 2