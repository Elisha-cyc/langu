from backend.ai.teacher import explain_text


class VocabularyEngine:

    def generate(
        self,
        passage,
        target_language,
        learner_level="Beginner"
    ):
        """
        Extract important vocabulary from any lesson.
        """

        return explain_text(
            text=passage,
            target_language=target_language,
            learner_level=learner_level,
            mode="vocabulary"
        )


if __name__ == "__main__":

    engine = VocabularyEngine()

    result = engine.generate(
        passage="こんにちは。私は学生です。",
        target_language="English",
        learner_level="Beginner"
    )

    print(result)