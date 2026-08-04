from flask import Flask, jsonify
from app.config.firebase import db

app = Flask(__name__)


@app.route("/test-firebase")
def test_firebase():

    db.collection("test").add({
        "message": "Hello Firebase3"
    })

    docs = db.collection("test").stream()

    messages = []

    for doc in docs:
        messages.append(doc.to_dict())

    return jsonify({
        "success": True,
        "data": messages
    })


if __name__ == "__main__":
    app.run(debug=True)