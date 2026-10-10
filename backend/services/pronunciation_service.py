# backend/services/pronunciation_service.py
import difflib
import os
import re
import unicodedata
import uuid
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from backend.config import USER_AUDIO_DIR

load_dotenv()


# Whisper expects ISO-639-1 codes. Twi is NOT supported by Whisper, so it is
# left out on purpose (scoring Twi would always be wrong).
LANGUAGE_CODES = {
    "arabic": "ar", "chinese": "zh", "dutch": "nl", "english": "en",
    "french": "fr", "german": "de", "greek": "el", "hebrew": "he",
    "hindi": "hi", "italian": "it", "japanese": "ja", "korean": "ko",
    "polish": "pl", "portuguese": "pt", "russian": "ru", "spanish": "es",
    "swedish": "sv", "thai": "th", "turkish": "tr", "vietnamese": "vi",
}

NO_SPACE_LANGUAGES = {"japanese", "chinese", "thai"}

NO_SPEECH_THRESHOLD = 0.6
MIN_AUDIO_BYTES = 2000


class PronunciationService:

    def __init__(self):
        self.audio_folder = USER_AUDIO_DIR
        self.audio_folder.mkdir(parents=True, exist_ok=True)

        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Pronunciation analysis requires "
                "a valid Groq API key in the environment (.env file)."
            )

        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )

    def supports(self, language):
        return (language or "").strip().lower() in LANGUAGE_CODES

    def analyze(self, audio_file, expected_text, language):
        expected_text = self._clean_expected(expected_text)
        language_key = (language or "").strip().lower()

        if language_key not in LANGUAGE_CODES:
            # Before: unknown languages (Twi, French, German...) were guessed
            # by Whisper's auto-detect and scored wrongly.
            return {
                "score": None,
                "supported": False,
                "feedback": (
                    f"Speaking scores are not available for {language or 'this language'} yet. "
                    "Listen to the audio, repeat it aloud, then mark the page as practiced."
                ),
                "expected": expected_text,
                "transcript": None,
                "language": language,
            }

        ext = Path(audio_file.filename or "").suffix or ".webm"
        save_path = self.audio_folder / f"{uuid.uuid4().hex}{ext}"
        audio_file.save(save_path)

        try:
            if save_path.stat().st_size < MIN_AUDIO_BYTES:
                return self._silence_result(expected_text, language)

            try:
                transcript, heard_speech = self._transcribe(save_path, language_key)
            except Exception as error:
                return {
                    "score": None,
                    "supported": True,
                    "feedback": "Couldn't analyze that recording. Please try again.",
                    "expected": expected_text,
                    "transcript": None,
                    "language": language,
                    "error": str(error),
                }

            if not heard_speech:
                return self._silence_result(expected_text, language)

            score = self._score(expected_text, transcript, language_key)

            return {
                "score": score,
                "supported": True,
                "feedback": self._feedback(score, expected_text, transcript),
                "expected": expected_text,
                "transcript": transcript,
                "language": language,
            }
        finally:
            try:
                save_path.unlink()
            except OSError:
                pass

    def _silence_result(self, expected_text, language):
        return {
            "score": 0,
            "supported": True,
            "feedback": (
                "We didn't hear any speech. Check your microphone, "
                "speak clearly, and try again."
            ),
            "expected": expected_text,
            "transcript": "",
            "language": language,
        }

    def _transcribe(self, save_path, language_key):
        with open(save_path, "rb") as audio:
            response = self.client.audio.transcriptions.create(
                model="whisper-large-v3",
                file=audio,
                response_format="verbose_json",
                temperature=0,
                language=LANGUAGE_CODES[language_key],
            )

        text = (getattr(response, "text", "") or "").strip()
        if not text:
            return "", False

        segments = getattr(response, "segments", None) or []

        if segments:
            speech = [
                s for s in segments
                if _seg(s, "no_speech_prob") <= NO_SPEECH_THRESHOLD
            ]

            if not speech:
                return "", False

            text = " ".join(
                str(_seg(s, "text", "")).strip() for s in speech
            ).strip()

        return text, bool(text)

    def _clean_expected(self, text):
        # Static lessons store steps as "japanese — romaji".
        return (text or "").split(" — ")[0].strip()

    def _normalize(self, text, language_key):
        text = unicodedata.normalize("NFKC", text or "").lower().strip()
        text = re.sub(r"[^\w\s]", "", text)
        text = re.sub(r"\s+", " ", text)

        if language_key in NO_SPACE_LANGUAGES:
            text = text.replace(" ", "")

        return text

    def _score(self, expected_text, transcript, language_key):
        expected_norm = self._normalize(expected_text, language_key)
        transcript_norm = self._normalize(transcript, language_key)

        if not expected_norm or not transcript_norm:
            return 0

        ratio = difflib.SequenceMatcher(
            None, expected_norm, transcript_norm
        ).ratio()

        return round(ratio * 100)

    def _feedback(self, score, expected_text, transcript):
        if score >= 95:
            return "Outstanding — what you said matched the target almost exactly."

        if score >= 85:
            return "Great job — very close to the target sentence."

        if score >= 70:
            return (
                f'Good attempt, but it sounded like "{transcript}" rather than '
                f'"{expected_text}". Listen again and try to match it more closely.'
            )

        if score >= 40:
            return (
                f'It sounded like you said "{transcript}", which is quite '
                f'different from "{expected_text}". Listen to the AI reading '
                "and try again slowly."
            )

        return (
            "We couldn't recognize enough of what was said to match it to the "
            "target sentence. Make sure you're recording clearly and try again."
        )


def _seg(segment, key, default=0.0):
    if isinstance(segment, dict):
        return segment.get(key, default)
    return getattr(segment, key, default)