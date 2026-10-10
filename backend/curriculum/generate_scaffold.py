# generate_scaffold.py
"""
Generates placeholder lesson files for every language/level.

Schema for each lesson dict:
{
    "lesson_number": int,
    "title": str,
    "vocabulary": [
        {"word": str, "translation": str, "pronunciation": str}, ...
    ],
    "grammar": {
        "topic": str,
        "explanation": str,
    },
    "example_sentences": [
        {"target_language": str, "english": str}, ...
    ],
    "exercises": [
        {"type": "translation" | "fill_in_blank" | "multiple_choice" | "matching",
         "prompt": str,
         "answer": str,
         "options": list  # only for multiple_choice, else omitted
        }, ...
    ],
}
"""

import os

LANGUAGES = [
    "german", "dutch", "italian", "korean", "russian", "spanish", "swedish",
    "greek", "french", "arabic", "chinese", "hindi", "hebrew", "polish",
    "portuguese", "thai", "twi", "vietnamese", "turkish",
]

LEVELS = ["beginner", "intermediate", "advanced"]

BASE_DIR = "/home/claude/language_lessons"

LESSON_TEMPLATE = '''    {{
        "lesson_number": {n},
        "title": "TODO: {level_cap} Lesson {n} title",
        "vocabulary": [
            {{"word": "TODO", "translation": "TODO", "pronunciation": "TODO"}},
        ],
        "grammar": {{
            "topic": "TODO",
            "explanation": "TODO",
        }},
        "example_sentences": [
            {{"target_language": "TODO", "english": "TODO"}},
        ],
        "exercises": [
            {{"type": "translation", "prompt": "TODO", "answer": "TODO"}},
        ],
    }},
'''

FILE_HEADER = '''"""
{lang_cap} - {level_cap} level
{count} lessons. See generate_scaffold.py for the lesson schema.
Fill in the TODO fields with real content.
"""

lessons = [
'''

FILE_FOOTER = "]\n"


def build_file(lang: str, level: str, num_lessons: int = 50) -> str:
    lang_cap = lang.capitalize()
    level_cap = level.capitalize()
    content = FILE_HEADER.format(lang_cap=lang_cap, level_cap=level_cap, count=num_lessons)
    for n in range(1, num_lessons + 1):
        content += LESSON_TEMPLATE.format(n=n, level_cap=level_cap)
    content += FILE_FOOTER
    return content


def main():
    for lang in LANGUAGES:
        lang_dir = os.path.join(BASE_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)
        for level in LEVELS:
            file_path = os.path.join(lang_dir, f"{level}.py")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(build_file(lang, level))
    print(f"Generated {len(LANGUAGES)} languages x {len(LEVELS)} levels x 50 lessons.")


if __name__ == "__main__":
    main()
