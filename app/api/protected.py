#08/08 - when I come back to this file,
#I need to be able to explain EVERYTHING in here
from flask import Blueprint, jsonify, request
from firebase_admin import auth

protected_bp = Blueprint("protected", __name__)

@protected_bp.route("/protected")
def protected():

    #get Bearer wsefiojwnwoekcm...
    auth_header = request.headers.get("Authorization", "")

    #if the format is invalid (No "Bearer"), return an error

    if not auth_header.startswith("Bearer "):
        return jsonify({
            "error": "Missing or invalid Authorisation header"
        }), 401
    print("Got valid token")

    #Extracts just the token part
    #id_token = auth_header.split("Bearer ", 1) gives us ["", "wefiwneofwefbi..."]
    #[1].strip() - gives us just the "weisehqnowef..." with no wxtra spaces.
    id_token = auth_header.split("Bearer ", 1)[1].strip()
    try:
        decoded_token = auth.verify_id_token(id_token)
    except Exception as error:
        return jsonify({
            "error": "Invalid token",
            "details": str(error)
        }), 401

    #print(decoded_token)
    #'iss': 'https://securetoken.google.com/german-learning-api', 'aud': 'german-learning-api', 'auth_time': ..., 'user_id': '...', 'sub': '...', 'iat': ..., 'exp': ..., 'email': '...', 'email_verified': T/False, 'firebase': {'identities': {'email': ['...']}, 'sign_in_provider': 'password'}, 'uid': '..'}
    #Use this pattern to get the user's ID
    uid = decoded_token.get("uid")
    print("User_id", uid)

    print("authentication succesful")
    return jsonify({
        "message": "Authenticated succesfully",
        "uid": uid
    }), 200


