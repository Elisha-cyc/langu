from backend.database.lesson_repository import create_official_book

OFFICIAL_BOOKS = [

    # Japanese
    ("Genki I", "Japanese", "Beginner", "Lingua AI", "genki1.jpg", "japanese/genki1.pdf"),
    ("JLPT N5 Grammar", "Japanese", "Beginner", "Lingua AI", "jlpt_n5.jpg", "japanese/jlpt_n5.pdf"),
    ("Japanese Short Stories", "Japanese", "Elementary", "Lingua AI", "stories.jpg", "japanese/stories.pdf"),

    # Chinese
    ("HSK 1 Standard Course", "Chinese", "Beginner", "Lingua AI", "hsk1.jpg", "chinese/hsk1.pdf"),
    ("Chinese Graded Reader", "Chinese", "Beginner", "Lingua AI", "reader.jpg", "chinese/reader.pdf"),

    # Korean
    ("Korean Made Easy", "Korean", "Beginner", "Lingua AI", "korean_easy.jpg", "korean/korean_easy.pdf"),
    ("Hangul Workbook", "Korean", "Beginner", "Lingua AI", "hangul.jpg", "korean/hangul.pdf"),

    # English
    ("English Grammar in Use", "English", "Intermediate", "Lingua AI", "grammar.jpg", "english/grammar.pdf"),
    ("Everyday Conversations", "English", "Beginner", "Lingua AI", "conversation.jpg", "english/conversation.pdf"),

    # Twi
    ("Twi For Beginners", "Twi", "Beginner", "Lingua AI", "twi.jpg", "twi/twi_beginner.pdf"),
    ("Speak Twi Daily", "Twi", "Elementary", "Lingua AI", "speak_twi.jpg", "twi/speak_twi.pdf"),

    # Spanish
    ("Spanish For Beginners", "Spanish", "Beginner", "Lingua AI", "spanish_beginner.jpg", "spanish/spanish_beginner.pdf"),
    ("Spanish Conversations", "Spanish", "Elementary", "Lingua AI", "spanish_talk.jpg", "spanish/conversations.pdf"),

    # Arabic
    ("Arabic Alphabet", "Arabic", "Beginner", "Lingua AI", "arabic_alphabet.jpg", "arabic/alphabet.pdf"),
    ("Modern Arabic Basics", "Arabic", "Beginner", "Lingua AI", "arabic_basics.jpg", "arabic/basics.pdf"),
]


def seed_books():

    print("=" * 40)
    print("Installing Official Lingua Library")
    print("=" * 40)

    for book in OFFICIAL_BOOKS:

        create_official_book(*book)

        print(f"✓ {book[0]}")

    print("=" * 40)
    print("Official Library Installed!")
    print("=" * 40)


if __name__ == "__main__":
    seed_books()