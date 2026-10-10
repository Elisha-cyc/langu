# backend/services/reading_service.py
import re


class ReadingService:

    def split_sentences(self, text):
        """
        Split text into readable teaching sentences.
        """

        if not text:
            return []

        pattern = r'(?<=[。！？.!?])\s*'

        sentences = re.split(pattern, text.strip())

        return [
            sentence.strip()
            for sentence in sentences
            if sentence.strip()
        ]


if __name__ == "__main__":

    service = ReadingService()

    result = service.split_sentences(
        "こんにちは。私は学生です。よろしくお願いします。"
    )

    print(result)