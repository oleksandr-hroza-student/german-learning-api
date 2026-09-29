from dotenv import load_dotenv

load_dotenv()
from app.config.firebase import initialize_firebase
from app.services.flashcard_service import create_flashcards_from_text
from app.repositories.noun_repository import lookup_noun


def main():
    initialize_firebase()
    user_id = ""

    word = "Universitätsbibliothekskaffeemaschinenwartungsvertragsverlängerungsantrag"

    print("Checking SQLite first...")

    sqlite_result = lookup_noun(word)

    print("SQLite result:", sqlite_result)

    if sqlite_result:
        print("This word exists in SQLite.")
        print("Choose another word if you want to test the AI fallback.")
        return

    print("\nWord not found in SQLite.")
    print("AI fallback should now be triggered.")

    created, skipped = create_flashcards_from_text(
        user_id,
        word
    )

    print("\nCreated:")
    print(created)

    print("\nSkipped:")
    print(skipped)


if __name__ == "__main__":
    main()

