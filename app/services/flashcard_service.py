"""
This file:
    Decides what gets created

it coordinates 2 existing pieces:

noun_service -> tells us which nouns are valid

flashcard_repository -> saves valid cards

What we want to do is:
    Create flash cards for the nouns that the user has not learnt yet and
    that return as valid words
"""

from app.services.noun_service import process_multiple_nouns
from app.repositories.flashcard_repository import create_flashcard

from app.repositories.flashcard_repository import get_all_flashcards, delete_flashcard

def create_flashcards_from_text(user_id, text):
    noun_results = process_multiple_nouns(text)
    #print(noun_results)

    created = []
    skipped = []

    for result in noun_results:
        if result["status"] == "not_found":
            skipped.append(result)
        elif result["status"] == "ambiguous":
            skipped.append(result)
             #Implement AI fallback later
        elif result["status"] == "gender_missing":
            skipped.append(result)
            #Implement AI fallback later
        elif result["status"] == "found":
            created_response = create_flashcard(user_id, result["word"], result["gender"])
            if created_response["status"] == "created":
                created.append(created_response)
            elif created_response["status"] == "already_exists":
                skipped.append(created_response)




    """
    print("Skipped ", skipped)
    print("Created", created)
    """
    return created, skipped

"""
Currently the service layer does not have a lot of functionality that would involve these 2 functions,
But we still pass the data throug the service layer in case we then later need to expand it.
All in the name of architectural consistency.
"""
def get_flashcards_for_user(user_id):
    return get_all_flashcards(user_id)

def delete_flashcard_for_user(user_id, card_id):
    return delete_flashcard(user_id, card_id)



#create_flashcards_from_text(1, "Hund HEHEHE katze Band")


