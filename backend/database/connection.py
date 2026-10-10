# connection.py
import sqlite3
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Database folder
DATABASE_DIR = PROJECT_ROOT / "data" / "database"

# Database file
DATABASE_PATH = DATABASE_DIR / "language.db"


def get_connection():
    # Create the folder automatically if it doesn't exist
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)

    # Enable foreign key support
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


if __name__ == "__main__":
    connection = get_connection()
    print("Database connected successfully!")
    connection.close()