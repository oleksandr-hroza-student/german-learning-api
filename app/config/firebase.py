import firebase_admin
import logging
from pathlib import Path
from firebase_admin import credentials, firestore
import os

from dotenv import load_dotenv

#See if can move to run.py for better efficiancy - 04/08 CHECK
load_dotenv()  # Load environment variables from .env file

#MOVE TO run.py when set up! 04/08/26 CHECK
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)


#__name__ - gives the name of the current module, app.config.firebase in this case, this way we make a separate logger for each module
logger = logging.getLogger(__name__)
print(__name__)

def initialize_firebase():

    #Only if firebase has not been initialised, as firebase can only be initialised once per app.
    if not firebase_admin._apps:

        #give a value from a variable stored in .env, so that we don't expose anything
        #Sensitive where version control is used
        cred_path = os.getenv("FIREBASE_CREDENTIALS")

        if not cred_path:
            raise ValueError("Set up FIREBASE_CREDENTIALS in yo .env file, be smart, work hard, love your family")

        #COnvert it into an object of type Path, to have more functionality
        cred_path = Path(cred_path)

        #to find the path to the firebase json file, starting at project root
        if not cred_path.is_absolute(): #(checks if that is a full system path)
            project_root = Path(__file__).resolve().parents[2]
            cred_path = project_root / cred_path # combines the paths

        #Creates a firebase credential object from the service account key file
        cred = credentials.Certificate(cred_path)



        firebase_admin.initialize_app(cred)
        logger.info("Firebase initialised successfully")


#init firebase itself - the method we have just written
initialize_firebase()

#Created a connection to the database.
#Now, if we want to access the db from anywherein the app, we type: from app.config.firebase import db
db = firestore.client()









