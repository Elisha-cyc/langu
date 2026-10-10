# detector.py
from groq import APIError, RateLimitError

from backend.ai.client import client
from backend.ai.models import TEACHING_MODEL


def detect_language(text):
    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    try:
        response = client.chat.completions.create(
            model=TEACHING_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a language detection assistant. "
                        "Identify the language of the given text. "
                        "Reply with ONLY the language name such as "
                        "English, Chinese, Japanese, Korean, French or Spanish."
                    )
                },
                {
                    "role": "user",
                    "content": text
                }
            ],
            temperature=0
        )

    except RateLimitError as error:
        raise RuntimeError(
            "Groq rate limit reached. Please try again later."
        ) from error

    except APIError as error:
        raise RuntimeError(
            f"Groq API Error: {error}"
        ) from error

    language = response.choices[0].message.content.strip()

    return language


if __name__ == "__main__":

    result = detect_language("我叫李明")

    print("Detected language:", result)