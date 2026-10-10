# translator.py
from groq import APIError, RateLimitError

from backend.ai.client import client
from backend.ai.models import TEACHING_MODEL


def translate_text(text, target_language):

    if not text or not text.strip():
        raise ValueError("Text cannot be empty.")

    if not target_language or not target_language.strip():
        raise ValueError("Target language cannot be empty.")

    try:
        response = client.chat.completions.create(
            model=TEACHING_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a professional multilingual translator. "
                        "Translate the user's text accurately and naturally. "
                        "Return ONLY the translated text with no explanations."
                    )
                },
                {
                    "role": "user",
                    "content": (
                        f"Translate this into {target_language}:\n\n{text}"
                    )
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

    translation = response.choices[0].message.content.strip()

    return translation


if __name__ == "__main__":

    result = translate_text(
        "我叫李明",
        "English"
    )

    print("Translation:", result)