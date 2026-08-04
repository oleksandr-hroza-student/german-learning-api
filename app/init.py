
#PEP 8:
#1.Standart library import
import logging

#2.related third party imports
from flask import Flask
from dotenv import load_dotenv

#3.Local app imports.
from app.config.firebase import initialize_firebase
from app.api.health_flask import health_bp
from app.api.health_firestore import health_firestore_bp





def create_app():
    #Configure logger once and for everything.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s"
    )

    # Load environment variables from .env file, better to do before any app configuration
    load_dotenv()

    # Create the Flask application
    app = Flask(__name__)

    #Configure application-later (secret keys, et)


    #Initilise services (only firebase for now, later we will add more)
    """Later, as the amount of services grows, it might make sence to create a separate module 'initilize_services()' and call it here"""
    initialize_firebase()


    #Register blueprints (health check, firestore test) later - authentication
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(health_firestore_bp, url_prefix="/api")

    return app