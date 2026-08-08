#08/08 - when I come back to this file,
#I need to be able to explain EVERYTHING in here
from flask import Blueprint, jsonify, request
from firebase_admin import auth

protected_bp = Blueprint("protected", __name__)

@protected_bp.route("/protected")
def protected():

    auth_header = request.headers.get("Authorisation", "")

    if not auth_header.strtwith("Bearer "):
        return jsonify({
            "error": "Missing or invalid Authorisation header"
        }), 401


    id_token = auth_header.split("Bearer ", 1)[1].strip()
