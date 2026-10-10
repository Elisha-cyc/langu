# grammar.py
from backend.ai.teacher import explain_text


class GrammarEngine:

    def generate(
        self,
        passage,
        target_language,
        learner_level="Beginner"
    ):
        """
        Explain the grammar used in a lesson.
        """

        return explain_text(
            text=passage,
            target_language=target_language,
            learner_level=learner_level,
            mode="grammar"
        )


if __name__ == "__main__":

    engine = GrammarEngine()

    result = engine.generate(
        passage="私は学生です。",
        target_language="English",
        learner_level="Beginner"
    )

    print(result)