#"Is my backend running?"
#If yes, it confirms that flask is running, the server can receive HTTP requests and if the routing works

from flask import Blueprint, jsonify

health_bp = Blueprint("health_flask", __name__)

@health_bp.route("/health_flask")
def health():
    return jsonify({"status": "ok"})

"""

Blueprints:
 "Extensions to the application", they allow you to separate the application into 
 different components and make it easier to manage.
 
(We don't need to create a new app in each file/ write everything in the same file.)
 
 In the main application file you would have:
 from health import health_bp
 ...
 app.register_blueprint(health_db, url_prefix="/api")
 (all routes in the blueprint would start with "/api")
 
 
"""



