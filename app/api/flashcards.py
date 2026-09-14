"""
This file:
    HTTP request/response
"""

from flask import Blueprint, jsonify, request, g

from app.auth.decorators import auth_required
from app.services.flashcard_service import create_flashcards_from_text, get_flashcards_for_user, delete_flashcard_for_user


flashcards_bp = Blueprint("flashcards", __name__)

@flashcards_bp.route("/flashcards", methods=["POST"])
@auth_required
def create_flashcards():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Text is required"
        }), 400

    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "error": "Text is required"
        }), 400

    user_id = g.uid

    created, skipped = create_flashcards_from_text(user_id, text)

    return jsonify({
        "created": created,
        "skipped": skipped
    }), 201

@flashcards_bp.route("/flashcards", methods=["GET"])
@auth_required
def get_flashcards():
    user_id = g.uid

    flashcards = get_flashcards_for_user(user_id)

    return jsonify({
        "flashcards": flashcards
    }), 200

"""
"/flashcards/<card_id>"
<card_id> - a dynamic URL parameter
eg:
    /api/flashcards/hund
    /api/flashcards/shule
"""


@flashcards_bp.route(
    "/flashcards/<card_id>",
    methods=["DELETE"]
)
@auth_required
def remove_flashcard(card_id):
    user_id = g.uid

    result = delete_flashcard_for_user(
        user_id,
        card_id
    )

    if result["status"] == "not_found":
        return jsonify(result), 404

    return jsonify(result), 200