# backend/services/lesson_detector.py
import re

class LessonDetector:

    def detect(self, pages):

        lessons = []
        current = None

        patterns = [
            r"^lesson\s+\d+",
            r"^chapter\s+\d+",
            r"^unit\s+\d+",
            r"^第\s*\d+\s*課",
            r"^第\s*\d+\s*章",
        ]

        for page_number, text in enumerate(pages, start=1):

            first_lines = text.splitlines()[:8]

            found = None

            for line in first_lines:

                clean = line.strip()

                for pattern in patterns:

                    if re.match(pattern, clean, re.IGNORECASE):
                        found = clean
                        break

                if found:
                    break

            if found:

                if current:
                    current["end_page"] = page_number - 1
                    lessons.append(current)

                current = {
                    "lesson_id": len(lessons) + 1,
                    "title": found,
                    "start_page": page_number,
                    "end_page": page_number,
                }

        if current:
            current["end_page"] = len(pages)
            lessons.append(current)

        if not lessons:
            lessons.append({
                "lesson_id": 1,
                "title": "Lesson 1",
                "start_page": 1,
                "end_page": len(pages),
            })

        return lessons