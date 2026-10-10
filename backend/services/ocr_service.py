# backend/services/ocr_service.py
from pathlib import Path
import easyocr


class OCRService:

    def __init__(self):
        # Cache loaded OCR models
        self.readers = {}

    def get_reader(self, language):

        language_map = {
            "English": ["en"],
            "Japanese": ["ja", "en"],
            "Chinese": ["ch_sim", "en"],
            "Korean": ["ko", "en"],
            "Arabic": ["ar", "en"],
            "Spanish": ["es", "en"],
            "French": ["fr", "en"],
            "German": ["de", "en"],
            "Italian": ["it", "en"],
            "Portuguese": ["pt", "en"],
            "Russian": ["ru", "en"],
            "Greek": ["el", "en"],
            "Hindi": ["hi", "en"],
            "Thai": ["th", "en"],
            "Vietnamese": ["vi", "en"],
            "Dutch": ["nl", "en"],
            "Swedish": ["sv", "en"],
            "Polish": ["pl", "en"],
            "Hebrew": ["he", "en"],
            "Turkish": ["tr", "en"],
            "Twi": ["en"]
        }

        if language not in language_map:
            raise ValueError(f"Unsupported language: {language}")

        langs = language_map[language]
        key = tuple(langs)

        if key not in self.readers:
            self.readers[key] = easyocr.Reader(
                langs,
                gpu=False
            )

        return self.readers[key]

    def scan_image(self, image_path, language="English"):

        path = Path(image_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Image not found: {path}"
            )

        reader = self.get_reader(language)

        results = reader.readtext(
            str(path),
            detail=0
        )

        text = "\n".join(results).strip()

        if not text:
            raise ValueError(
                "No readable text was found in the image."
            )

        return text

    def supported_languages(self):

        return [
            "Japanese",
            "Chinese",
            "Korean",
            "Arabic",
            "Spanish",
            "French",
            "German",
            "Italian",
            "Portuguese",
            "Russian",
            "Turkish",
            "Greek",
            "Dutch",
            "Swedish",
            "Polish",
            "Hebrew",
            "Hindi",
            "Thai",
            "Vietnamese",
            "English",
            "Twi"
        ]


if __name__ == "__main__":

    ocr = OCRService()

    print("Supported Languages")
    print("-------------------")

    for language in ocr.supported_languages():
        print(language)

    print("\nScanning...\n")

    text = ocr.scan_image(
        "data/scans/images.jpg",
        language="Japanese"
    )

    print(text)