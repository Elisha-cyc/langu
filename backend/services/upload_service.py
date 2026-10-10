# backend/services/upload_service.py
from pathlib import Path
import shutil


class UploadService:

    def __init__(self):
        self.library = Path("data") / "library"
        self.library.mkdir(parents=True, exist_ok=True)

        self.allowed_extensions = [".pdf", ".docx"]

    def save_file(self, source_path):

        source = Path(source_path)

        if not source.exists():
            raise FileNotFoundError(
                f"File not found: {source}"
            )

        if source.suffix.lower() not in self.allowed_extensions:
            raise ValueError(
                "Only PDF and DOCX files are supported."
            )

        destination = self.library / source.name

        # Prevent overwriting an existing file
        if destination.exists():

            counter = 1

            while True:

                new_name = (
                    f"{source.stem}_{counter}"
                    f"{source.suffix}"
                )

                destination = self.library / new_name

                if not destination.exists():
                    break

                counter += 1

        shutil.copy2(source, destination)

        return destination.name

    def get_library_path(self):
        return self.library


if __name__ == "__main__":

    upload = UploadService()

    print("Upload service ready!")

    print("Library location:")

    print(upload.get_library_path())