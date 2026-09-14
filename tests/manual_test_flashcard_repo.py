import os
from pathlib import Path

from dotenv import load_dotenv

from app.config.firebase import initialize_firebase
from app.repositories.flashcard_repository import create_flashcard


def main():
    project_root = Path(__file__).resolve().parents[1]

    load_dotenv(project_root / ".env")
    load_dotenv(project_root / ".env.test")

    test_user_id = os.getenv("TEST_USER_UID")

    assert test_user_id is not None, "TEST_USER_UID not loaded"

    initialize_firebase()

    print(create_flashcard(
        test_user_id,
        "Hund",
        "m"
    ))

    print(create_flashcard(
        test_user_id,
        "Hund",
        "m"
    ))


if __name__ == "__main__":
    main()