"""
This file:
    HTTP request/response
"""

from flask import Blueprint, jsonify, request, g

from app.auth.decorators import auth_required
from app.services.flashcard_service import create_flashcards_from_text


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

