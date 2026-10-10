# backend/lessons/exercises.py
from backend.ai.teacher import explain_text


class ExerciseEngine:

    def generate(
        self,
        passage,
        target_language,
        learner_level="Beginner"
    ):
        """
        Generate AI exercises from any lesson.
        """

        return explain_text(
            text=passage,
            target_language=target_language,
            learner_level=learner_level,
            mode="exercise"
        )


if __name__ == "__main__":

    engine = ExerciseEngine()

    result = engine.generate(
        passage="こんにちは。私は学生です。",
        target_language="English",
        learner_level="Beginner"
    )

    print(result)