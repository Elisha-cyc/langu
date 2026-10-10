# backend/services/profile_service.py
from backend.database.user_repository import (
    create_user,
    get_user,
    update_user_profile
)


class ProfileService:

    def create_profile(
        self,
        name,
        native_language,
        learning_language,
        learner_level
    ):

        user_id = create_user(
            name=name,
            native_language=native_language,
            learning_language=learning_language,
            learner_level=learner_level
        )

        return {
            "success": True,
            "user_id": user_id,
            "message": "Profile created successfully."
        }

    def get_profile(self, user_id):

        user = get_user(user_id)

        if not user:
            raise ValueError("User not found.")

        return {
            "id": user[0],
            "name": user[1],
            "native_language": user[2],
            "learning_language": user[3],
            "learner_level": user[4],
            "xp": user[5],
            "created_at": user[6]
        }

    def update_profile(
        self,
        user_id,
        native_language,
        learning_language,
        learner_level
    ):

        update_user_profile(
            user_id=user_id,
            native_language=native_language,
            learning_language=learning_language,
            learner_level=learner_level
        )

        return self.get_profile(user_id)


if __name__ == "__main__":

    service = ProfileService()

    result = service.create_profile(
        name="Elisha",
        native_language="Twi",
        learning_language="Japanese",
        learner_level="Intermediate"
    )

    print(result)