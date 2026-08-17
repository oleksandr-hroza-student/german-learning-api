from flask import Blueprint, jsonify, g, request
from app.auth.decorators import auth_required
from app.config.firebase import get_db
me_bp = Blueprint("me", __name__)

"""
Flow of the /me route:

1. Call get_me()
2. get_me points to a wrapper
3. wrapper (auth_required) executes:
    a.Read the sutorisetion header
    b.Veryfi Firebase token
    c. Store the user ID in g.uid
    d. Call the original route function 
    (get_me)
4.get_me reads the g.uid
    --Because g.uid is a request-scope variable, get_me can also see it. it can not access any other into from the wrapper, as it is function scope (unless you intentionally pass it into the function)
5.get_me returns the user data
..(to be continued.)
"""

@me_bp.route("/me", methods = ["POST"])
@auth_required
def create_me():
    data = request.get_json()
    username = data.get("username", "").strip()

    if not username:
        username = "temp_username"

    user_id = g.uid
    user_ref = get_db().collection("users").document(user_id)

    user_doc = user_ref.get()

    if user_doc.exists:
        return jsonify({
            "error": "User profile already exists"
        }), 409
    else:
        user_ref.set({
            "streak":0,
            "username": username
        })

        return jsonify({
            "message": "User profile created"
        }), 201











@me_bp.route("/me", methods = ["GET"])
@auth_required
def get_me():
    user_id = g.uid  # Get the user ID from the global context set by the decorator
    #returns firestore db -> points to collection "users" -> points to the specific user document, result stored in user_ref
    #user_ref - basically just a reference, does not contain document data
    user_ref = get_db().collection("users").document(user_id)
    #Get the user's document using the reference derived earlier
    #The object itself is a Firestore DocumentSnapshot, which we can later convert into a dict
    user_doc = user_ref.get()

    if not user_doc.exists:
        return jsonify({
            "error": "User profile not found"
        }), 404

    return jsonify(user_doc.to_dict()), 200