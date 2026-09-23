from flask import Blueprint, request, jsonify, g

from app.auth.decorators import auth_required
from app.services.review_service import process_review_session

reviews_bp = Blueprint("reviews", __name__)

"""
Example input format:

{
  "timezone": "Europe/Dublin",
  "review_results": [
    {
      "card_id": "Hund",
      "decision": "OK",
      "again_count": 0
    },
    {
      "card_id": "Katze",
      "decision": "EASY",
      "again_count": 1
    }
  ]
}
"""




@reviews_bp.route("/review/session", methods=["POST"])
@auth_required
def submit_review_session():
    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    timezone_name = data.get("timezone")
    review_results = data.get("review_results")

    if not timezone_name:
        return jsonify({
            "error": "Timezone is required"
        }), 400

    if not isinstance(review_results, list):
        return jsonify({
            "error": "review_results must be a list"
        }), 400

    if len(review_results) == 0:
        return jsonify({
            "error": "review_results must not be empty"
        }), 400

    for review in review_results:
        if not isinstance(review, dict):
            return jsonify({
                "error": "Each review result must be an object"
            }), 400


        if "card_id" not in review:
            return jsonify({
                "error": "Each review must contain a card_id"
            }), 400

        if not review.get("card_id"):
            return jsonify({
                "error": "Each review must contain a card_id"
            }), 400


        if "decision" not in review:
            return jsonify({
                "error": "Each review result must contain decision"
            }), 400

        if review["decision"] not in ["OK", "EASY"]:
            return jsonify({
                "error": "Decision must be OK or EASY"
            }), 400

        again_count = review.get("again_count", 0)

        if not isinstance(again_count, int) or again_count < 0:
            return jsonify({
                "error": "again_count must be a non-negative integer"
            }), 400

    results = process_review_session(
        g.uid,
        review_results,
        timezone_name
    )

    return jsonify({
        "results": results
    }), 200
