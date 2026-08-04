"""
The purpuse of this file is to simply run the app.
It does not contain any logic, or needs to know what gous into building the app

"""

from app.init import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
