# teacher.py
import json
import re

from groq import APIError, RateLimitError

from backend.ai.client import client
from backend.ai.models import TEACHING_MODEL
from backend.ai.prompt_manager import TEACHER_STEPS_PROMPT


# =====================================================
# TOKEN SETTINGS
# =====================================================

TEACH_TOKENS_PER_SENTENCE = 1200
TEACH_TOKENS_MIN = 2500
TEACH_TOKENS_MAX = 16000
SUMMARY_TOKENS = 1500


# =====================================================
# PROMPTS FOR SUMMARY / KEY POINTS
# =====================================================

SUMMARY_PROMPT = """You are a language-learning assistant.
The learner's level is {learner_level}. Write your answer in {target_language}.
The passage may be in any language ({learning_language}).

Return ONLY a JSON object in this exact shape:
{{
  "summary": "A short, clear summary of the passage.",
  "key_points": ["Key point 1", "Key point 2", "Key point 3"]
}}

Use simple wording suited to the learner's level."""


# =====================================================
# HELPERS
# =====================================================

def validate_input(text):
    if not text or not text.strip():
        raise ValueError("The passage cannot be empty.")


def estimate_sentence_count(text):
    matches = re.findall(r"[.!?。！？]+", text)
    return max(len(matches), 1)


def max_tokens(text):
    count = estimate_sentence_count(text)
    budget = TEACH_TOKENS_MIN + count * TEACH_TOKENS_PER_SENTENCE
    return min(budget, TEACH_TOKENS_MAX)


def stringify_vocab(item):
    if isinstance(item, dict):
        word = item.get("word", "")
        meaning = item.get("meaning", "")
        return f"{word} ({meaning})" if meaning else word
    return str(item)


def build_context(context):
    if not context:
        return ""

    vocabulary = context.get("known_vocabulary", [])
    grammar = context.get("known_grammar", [])
    events = context.get("key_events", [])

    if not (vocabulary or grammar or events):
        return ""

    vocab_text = ", ".join(stringify_vocab(v) for v in vocabulary)

    return f"""
Learner Progress

Vocabulary already learned:
{vocab_text or "None"}

Grammar already learned:
{", ".join(grammar) or "None"}

Previous lesson context:
{" | ".join(events) or "None"}

"""


def call_model(system_prompt, user_prompt, tokens):
    """One place for the Groq call and its error handling."""
    try:
        response = client.chat.completions.create(
            model=TEACHING_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2,
            max_completion_tokens=tokens,
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

    except RateLimitError as error:
        raise RuntimeError(
            "Groq rate limit reached. Please try again later."
        ) from error

    except APIError as error:
        raise RuntimeError(f"Groq API Error: {error}") from error


# =====================================================
# MAIN AI FUNCTION
# =====================================================

def explain_text(
    text,
    target_language="English",
    learner_level="Beginner",
    mode="teach",
    context=None,
    learning_language="Auto"
):
    validate_input(text)

    # ---------- Summary / key points ----------
    if mode in ("summary", "key_points"):
        prompt = SUMMARY_PROMPT.format(
            target_language=target_language,
            learner_level=learner_level,
            learning_language=learning_language
        )

        try:
            result = call_model(prompt, f"Passage:\n\n{text}", SUMMARY_TOKENS)
        except json.JSONDecodeError:
            result = {
                "summary": "AI could not generate a structured summary.",
                "key_points": []
            }

        result["explained_in"] = target_language
        return result

    # ---------- Step-by-step teaching ----------
    prompt = TEACHER_STEPS_PROMPT.format(
        target_language=target_language,
        learner_level=learner_level
    )

    user_prompt = f"""
{build_context(context)}

Passage:

{text}
"""

    try:
        result = call_model(prompt, user_prompt, max_tokens(text))
    except json.JSONDecodeError:
        result = {
            "steps": [
                {
                    "sentence": text,
                    "teaching": {
                        "translation": "AI could not generate structured JSON.",
                        "vocabulary": [],
                        "grammar": "",
                        "pronunciation": "",
                        "examples": [],
                        "practice": ""
                    }
                }
            ]
        }

    result["explained_in"] = target_language
    return result


# =====================================================
# RESULT FORMATTING
# =====================================================

def result_to_text(mode, result):
    """Turn an explain_text() result into plain text for the app."""
    if not result or not isinstance(result, dict):
        return ""

    if mode == "summary":
        return str(result.get("summary", "")).strip()

    if mode == "key_points":
        points = result.get("key_points") or []
        if points:
            return "\n".join(f"• {p}" for p in points)
        return str(result.get("summary", "")).strip()

    # Fallback for "teach" results, in case anything else calls this
    parts = []
    for index, step in enumerate(result.get("steps", []), start=1):
        teaching = step.get("teaching", {}) or {}
        lines = [f"Step {index}: {step.get('sentence', '')}"]
        if teaching.get("translation"):
            lines.append(f"Translation: {teaching['translation']}")
        if teaching.get("grammar"):
            lines.append(f"Grammar: {teaching['grammar']}")
        parts.append("\n".join(lines))
    return "\n\n".join(parts)


# =====================================================
# TEST
# =====================================================

if __name__ == "__main__":
    result = explain_text(
        text="こんにちは。私は学生です。",
        target_language="English",
        learner_level="Beginner"
    )

    print(json.dumps(result, indent=2, ensure_ascii=False))