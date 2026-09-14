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
