# backend/services/scan_service.py
from pathlib import Path


class ScanService:

    def __init__(self):

        self.scan_folder = Path("data") / "scans"

        self.scan_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        self.allowed_extensions = [
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        ]

    def save_scan(self, image_path):

        image = Path(image_path)

        if image.suffix.lower() not in self.allowed_extensions:
            raise ValueError("Unsupported image format.")

        destination = self.scan_folder / image.name

        destination.write_bytes(image.read_bytes())

        return str(destination)

    def list_scans(self):

        scans = []

        for image in self.scan_folder.iterdir():

            if image.suffix.lower() not in self.allowed_extensions:
                continue

            scans.append({
                "name": image.name,
                "path": str(image),
                "size_kb": round(image.stat().st_size / 1024, 1)
            })

        return scans