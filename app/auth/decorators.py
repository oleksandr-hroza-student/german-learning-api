from functools import wraps

from flask import g, jsonify, request
from firebase_admin import auth

def auth_required(route_function):
    @wraps(route_function)
    #*args & *kwargs - accepts whatever arguments the original route received.
    #*args - all positional arguments
    #*kwargs - all keyword arguments
    def wrapper(*args, **kwargs):
        #1. Read Authorization header
        auth_header = request.headers.get("Authorization", "")

        #2. Check Bearer format
        if not auth_header.startswith("Bearer "):
            return jsonify({
                "error": "Missing or invalid Authorisation header"
            }), 401
        print("Got valid token")

        #3. Extract token
        id_token = auth_header.split("Bearer ", 1)[1].strip()
        #4. Verify token
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception as error:
            return jsonify({
                "error": "Invalid token",
                "details": str(error)
            }), 401

        #5. Store uid in g
        g.uid = decoded_token["uid"]

        #6. Call the original route


        return route_function(*args, **kwargs)

    return wrapper