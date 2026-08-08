#Confirms the connection with firestore and the ability to read from it & write into it.
import logging
import time
from flask import Blueprint, jsonify
from app.config.firebase import get_db


health_firestore_bp = Blueprint("firestore_test", __name__)


logger = logging.getLogger(__name__)

@health_firestore_bp.route("/health_firestore")
def firestore_test():
    db = get_db()  # Get the Firestore database connection
    #Write in a test doc:

    db.collection("health_check").document("firestore_health_test").set(
        {
            "status": "connected",
            "message": "Hello, Firebase! (from /firestore_test)",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        }
    )

    doc = db.collection("health_check").document("firestore_health_test").get()

    if not doc.exists:
        logger.error("Failed to read from Firestore.")
        return jsonify({
            "success": False,
            "message": "Failed to read from Firestore."
        }), 500

    logger.info("Firestore connection successful!")

    return jsonify({
        "success": True,
        "message": "Firestore connection successful!",
        "data": doc.to_dict()
    })



