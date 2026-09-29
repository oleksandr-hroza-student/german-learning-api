from dotenv import load_dotenv

load_dotenv()

from app.services.ai_noun_service import resolve_noun_with_ai


def main():
    words = [
        "Miete",
        "Hund",
        "Band",
        "Blorpo"
    ]

    for word in words:
        print(f"\nTesting: {word}")

        result = resolve_noun_with_ai(word)

        print(result)


if __name__ == "__main__":
    main()