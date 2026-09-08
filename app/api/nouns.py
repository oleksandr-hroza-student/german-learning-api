from flask import Blueprint, jsonify, g, request
from app.auth.decorators import auth_required
from app.config.firebase import get_db
from app.services import noun_service

nouns_bp = Blueprint("nouns", __name__)

@nouns_bp.route("/nouns/process", methods = ["POST"])
@auth_required
def process_nouns():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    text = data.get("text", "").strip()

    if not text:
        return jsonify({
            "error": "Text is required"
        }), 400

    results = noun_service.process_multiple_nouns(text)

    return jsonify(results), 200







