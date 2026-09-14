"""
This file:
    Writes/Reads Firestore
"""

from app.config.firebase import get_db

def create_flashcard(user_id, word, gender):
    db = get_db()

    card_id = word.casefold()

    card_ref = (
        db.collection("users")
        .document(user_id)
        .collection("flashcards")
        .document(card_id)
    )

    card_doc = card_ref.get()
    if card_doc.exists:
        return {
            "status" : "already_exists",
            "word" : word
        }

    #if this fails, an exception will be visible.
    card_ref.set({
        "word" : word,
        "gender" : gender
    })


    return {
        "status" : "created",
        "word" : word,
        "gender" : gender
    }

def get_all_flashcards(user_id):
    db = get_db()

    cards_ref = (
        db.collection("users")
        .document(user_id)
        .collection("flashcards")
    )
    """
    Goes through all the documents in the collection,
    While cards_ref.get() only get's one record
    """
    docs = cards_ref.stream()

    flashcards = []

    for doc in docs:
        card = doc.to_dict()

        flashcards.append(card)

    return flashcards


def delete_flashcard(user_id, card_id):
    db = get_db()

    card_ref = (
        db.collection("users")
        .document(user_id)
        .collection("flashcards")
        .document(card_id.casefold())
    )

    card_doc = card_ref.get()

    if not card_doc.exists:
        return {
            "status": "not_found",
            "card_id": card_id
        }

    card_ref.delete()

    return {
        "status": "deleted",
        "card_id": card_id
    }
