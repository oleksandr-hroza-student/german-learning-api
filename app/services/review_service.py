from datetime import datetime, timezone

from app.services.review_scheduler import process_review
from app.repositories.flashcard_repository import (
    get_flashcard,
    update_flashcard_review
)


def review_flashcard(user_id, card_id, decision, timezone_name, reset_interval = False):

    card = get_flashcard(user_id, card_id)

    if card is None:
        return {
            "status": "not_found",
            "card_id": card_id
        }

    next_review_at = card.get("next_review_at")

    if next_review_at is not None and next_review_at > datetime.now(timezone.utc):
        return {
            "status": "not_due",
            "card_id": card_id
        }

    #0 acts as a default value in case the card doesn't have an interval_days field yet
    current_interval = card.get("interval_days", 0)

    if reset_interval:
        current_interval = 0

    review_result = process_review(
        current_interval,
        decision,
        datetime.now(timezone.utc),
        timezone_name)

    return update_flashcard_review(
        user_id,
        card_id,
        review_result["interval_days"],
        review_result["next_review_at"]
    )

def process_review_session(user_id, reviews, timezone_name):
    results = []

    for review in reviews:
        result = review_flashcard(
            user_id,
            review["card_id"],
            review["decision"],
            timezone_name,
            reset_interval=review.get("again_count", 0) > 0
        )

        results.append(result)

    return results